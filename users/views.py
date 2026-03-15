from django.db import transaction
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from rest_framework.generics import CreateAPIView
from django.utils import timezone
from rest_framework.views import APIView
from . import utils

from .serializers import ( RegisterValidateSerializer,AuthValidateSerializer,ConfirmationSerializer)

from users.models import CustomUser

from users import serializers
from rest_framework_simplejwt.views import TokenObtainPairView
from users.tasks import add, send_otp_email

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = serializers.CustomTokenObtainPairSerializer


class AuthorizationAPIView(CreateAPIView):
    serializer_class = AuthValidateSerializer

    def post(self, request):
        serializer = AuthValidateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = authenticate(**serializer.validated_data)

        if user:
            if not user.is_active:
                return Response(
                    status=status.HTTP_401_UNAUTHORIZED,
                    data={'error': 'User account is not activated yet!'}
                )

            token, _ = Token.objects.get_or_create(user=user)
            return Response(data={'key': token.key})

        return Response(
            status=status.HTTP_401_UNAUTHORIZED,
            data={'error': 'User credentials are wrong!'}
        )


class RegistrationAPIView(CreateAPIView):
    serializer_class = RegisterValidateSerializer

    def post(self, request, *args, **kwargs):
        add.delay(2,2)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data['email']
        password = serializer.validated_data['password']
        phone_number = serializer.validated_data['phone_number']

        user = CustomUser.objects.create_user(email=email, password=password, phone_number=phone_number, is_active=False)

        code = utils.generate_confirmation_code()
        utils.save_code_to_cache(user.email, code)
        print("Code generated and saved to cache.")

        print(f'Код подтверждения для пользователя {email}: {code}')  # Для отладки

        send_otp_email.delay(email, code)

        return Response(
            {'user_id': user.id, 'detail': 'Пользователь создан. Проверьте код подтверждения.'},
            status=status.HTTP_201_CREATED
        )


class ConfirmUserAPIView(CreateAPIView):
    serializer_class = ConfirmationSerializer

    def post(self, request):
        serializer = ConfirmationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user_id = serializer.validated_data['user_id']

        with transaction.atomic():
            user = CustomUser.objects.get(id=user_id)
            user.is_active = True
            user.save()

            token, _ = Token.objects.get_or_create(user=user)

        #    ConfirmationCode.objects.filter(user=user).delete()

        return Response(
            status=status.HTTP_200_OK,
            data={
                'message': 'User аккаунт успешно активирован',
                'key': token.key
            }
        )



class GoogleLoginAPIView(APIView):
    def post(self, request):
        data = request.data.get("google_data", {})

        user, _ = CustomUser.objects.get_or_create(email=data["email"])

        user.first_name = data.get("given_name")
        user.last_name = data.get("family_name")
        user.is_active = True
        user.last_login = timezone.now()
        user.registration_source = "google"
        user.save()

        token, _ = Token.objects.get_or_create(user=user)

        return Response({"key": token.key})

