from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from users.models import CustomUser
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from . import utils

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token["email"] = user.email
        token["birthdate"] = (
            user.birthdate.isoformat() if user.birthdate else None
        )
        return token

class UserBaseSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()


class AuthValidateSerializer(UserBaseSerializer):
    pass


class RegisterValidateSerializer(UserBaseSerializer):
    phone_number = serializers.CharField(required=False, allow_blank=True)

    def validate_email(self, email):
        if CustomUser.objects.filter(email=email).exists():
            raise ValidationError('CustomUser уже существует!')
        return email

    def validate(self, attrs):
        """
        Проверка: phone_number обязателен только для суперпользователя
        """
        is_superuser = attrs.get('is_superuser', False)
        phone_number = attrs.get('phone_number', None)

        if is_superuser and not phone_number:
            raise ValidationError({
                "phone_number": "Номер телефона обязателен для суперпользователя"
            })
        return attrs


class ConfirmationSerializer(serializers.Serializer):
    user_id = serializers.IntegerField()
    code = serializers.CharField(max_length=6)

    def validate(self, attrs):
        user_id = attrs.get('user_id')
        code = attrs.get('code')

        try:
            user = CustomUser.objects.get(user_id=user_id)
        except CustomUser.DoesNotExist:
            raise serializers.ValidationError("Пользователь не найден")

        if not utils.verify_confirmation_code(user_id, code):
            raise serializers.ValidationError("Неверный код подтверждения")

        attrs['user'] = user
        return attrs

    def save(self, **kwargs):
        user = self.validated_data['user']
        user.is_active = True
        user.save()


class OauthCodeSerializer(serializers.Serializer):
    code = serializers.CharField()