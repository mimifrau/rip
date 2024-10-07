from django.contrib.auth.models import User
from django.db import connection
from django.shortcuts import render, redirect
from django.utils import timezone

from app.models import Code, Tax, CodeTax


def index(request):
    code_name = request.GET.get("code_name", "")
    codes = Code.objects.filter(status=1)

    if code_name:
        codes = codes.filter(name__icontains=code_name)

    draft_tax = get_draft_tax()

    context = {
        "code_name": code_name,
        "codes": codes
    }

    if draft_tax:
        context["codes_count"] = len(draft_tax.get_codes())
        context["draft_tax"] = draft_tax

    return render(request, "home_page.html", context)


def add_code_to_draft_tax(request, code_id):
    code = Code.objects.get(pk=code_id)

    draft_tax = get_draft_tax()

    if draft_tax is None:
        draft_tax = Tax.objects.create()
        draft_tax.owner = get_current_user()
        draft_tax.date_created = timezone.now()
        draft_tax.save()

    if CodeTax.objects.filter(tax=draft_tax, code=code).exists():
        return redirect("/")

    item = CodeTax(
        tax=draft_tax,
        code=code
    )
    item.save()

    return redirect("/")


def code_details(request, code_id):
    context = {
        "code": Code.objects.get(id=code_id)
    }

    return render(request, "code_page.html", context)


def delete_tax(request, tax_id):
    if not Tax.objects.filter(pk=tax_id).exists():
        return redirect("/")

    with connection.cursor() as cursor:
        cursor.execute("DELETE FROM code_tax WHERE tax_id = %s", [tax_id])
        cursor.execute("DELETE FROM taxs WHERE id = %s", [tax_id])

    return redirect("/")


def tax(request, tax_id):
    if not Tax.objects.filter(pk=tax_id).exists():
        return redirect("/")

    context = {
        "tax": Tax.objects.get(id=tax_id),
    }

    return render(request, "tax_page.html", context)


def get_draft_tax():
    return Tax.objects.filter(status=1).first()


def get_current_user():
    return User.objects.filter(is_superuser=False).first()

from django.shortcuts import render, get_object_or_404
from .models import Tax  # Импортируйте вашу модель Tax
from django.utils import timezone
from dateutil.relativedelta import relativedelta

def tax(request, tax_id):
    tax = get_object_or_404(Tax, id=tax_id)
    selected_period = None
    start_date = None
    end_date = timezone.now()

    if request.method == 'POST':
        selected_period = int(request.POST.get('period', 0))
        if selected_period:
            start_date = end_date - relativedelta(months=selected_period)

    return render(request, 'tax_page.html', {
        'tax': tax,
        'selected_period': selected_period,
        'start_date': start_date,
        'end_date': end_date,
    })
