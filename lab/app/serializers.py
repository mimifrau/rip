from rest_framework import serializers

from .models import *


class CodeSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()

    def get_image(self, code):
        return code.image.url.replace("minio", "localhost", 1)

    class Meta:
        model = Code
        fields = "__all__"


class CodeItemSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()
    value = serializers.SerializerMethodField()

    def get_image(self, code):
        return code.image.url.replace("minio", "localhost", 1)

    def get_value(self, code):
        return self.context.get("value")

    class Meta:
        model = Code
        fields = ("id", "name", "image", "value")


class TaxSerializer(serializers.ModelSerializer):
    codes = serializers.SerializerMethodField()
    owner = serializers.SerializerMethodField()
    moderator = serializers.SerializerMethodField()

    def get_owner(self, tax):
        return tax.owner.username

    def get_moderator(self, tax):
        if tax.moderator:
            return tax.moderator.username
            
    def get_codes(self, tax):
        items = CodeTax.objects.filter(tax=tax)
        return [CodeItemSerializer(item.code, context={"value": item.value}).data for item in items]

    class Meta:
        model = Tax
        fields = '__all__'


class TaxsSerializer(serializers.ModelSerializer):
    owner = serializers.SerializerMethodField()
    moderator = serializers.SerializerMethodField()

    def get_owner(self, tax):
        return tax.owner.username

    def get_moderator(self, tax):
        if tax.moderator:
            return tax.moderator.username

    class Meta:
        model = Tax
        fields = "__all__"


class CodeTaxSerializer(serializers.ModelSerializer):
    class Meta:
        model = CodeTax
        fields = "__all__"


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'email', 'username')


class UserRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'email', 'password', 'username')
        write_only_fields = ('password',)
        read_only_fields = ('id',)

    def create(self, validated_data):
        user = User.objects.create(
            email=validated_data['email'],
            username=validated_data['username']
        )

        user.set_password(validated_data['password'])
        user.save()

        return user


class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True)
