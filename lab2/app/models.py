from django.db import models
from django.utils import timezone

from django.contrib.auth.models import User

from app.utils import STATUS_CHOICES


class Code(models.Model):
    STATUS_CHOICES = (
        (1, 'Действует'),
        (2, 'Удалена'),
    )

    name = models.CharField(max_length=100, verbose_name="Название")
    status = models.IntegerField(choices=STATUS_CHOICES, default=1, verbose_name="Статус")
    image = models.ImageField(default="images/default.png")
    description = models.TextField(verbose_name="Описание", blank=True)

    decryption = models.CharField(blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Продукт"
        verbose_name_plural = "Продукты"
        db_table = "codes"


class Tax(models.Model):
    status = models.IntegerField(choices=STATUS_CHOICES, default=1, verbose_name="Статус")
    date_created = models.DateTimeField(default=timezone.now(), verbose_name="Дата создания")
    date_formation = models.DateTimeField(verbose_name="Дата формирования", blank=True, null=True)
    date_complete = models.DateTimeField(verbose_name="Дата завершения", blank=True, null=True)

    owner = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Пользователь", null=True, related_name='owner')
    moderator = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Модератор", null=True, related_name='moderator')

    date = models.DateField(blank=True, null=True)

    def __str__(self):
        return "Заказ №" + str(self.pk)

    def get_codes(self):
        return [
            setattr(item.code, "value", item.value) or item.code
            for item in CodeTax.objects.filter(tax=self)
        ]

    def get_status(self):
        return dict(STATUS_CHOICES).get(self.status)

    class Meta:
        verbose_name = "Заказ"
        verbose_name_plural = "Заказы"
        ordering = ('-date_formation', )
        db_table = "taxs"


class CodeTax(models.Model):
    code = models.ForeignKey(Code, models.DO_NOTHING, blank=True, null=True)
    tax = models.ForeignKey(Tax, models.DO_NOTHING, blank=True, null=True)
    value = models.IntegerField(verbose_name="Поле м-м", blank=True, null=True)

    def __str__(self):
        return "м-м №" + str(self.pk)

    class Meta:
        verbose_name = "м-м"
        verbose_name_plural = "м-м"
        db_table = "code_tax"
