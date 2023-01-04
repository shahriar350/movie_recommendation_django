from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from django.core.validators import RegexValidator
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from django.core.validators import MinLengthValidator
from auth_app.models import Users

User = get_user_model()


class userInfoInitSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=255)
    phone_number = serializers.CharField(max_length=11)


class LoginSerializer(serializers.Serializer):
    phone_number = serializers.CharField(max_length=11, min_length=11,
                                         validators=[
                                             RegexValidator(
                                                 regex='(^(01)[3-9]\d{8})$',
                                                 message='Phone number is invalid format. Example: 01752495467',
                                                 code='invalid_username'
                                             ),
                                         ]
                                         )
    id = serializers.IntegerField(read_only=True)
    password = serializers.CharField(min_length=6)


class Registererializer(serializers.ModelSerializer):
    active = serializers.BooleanField(read_only=True)
    password = serializers.CharField(write_only=True, min_length=6)

    class Meta:
        model = User
        fields = ['id', 'name', 'phone_number', 'password', 'active']

    def validate_phone_number(self, data):
        if Users.objects.filter(phone_number=data).exists():
            raise ValidationError("This phone number is already used by another user.")
        return data

    def create(self, validated_data):
        validated_data['password'] = make_password(validated_data.get('password'))
        return super(Registererializer, self).create(validated_data)
