from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.core.exceptions import ValidationError

from users.managers import CustomUserManager


# Create your models here.

class CustomUser(AbstractBaseUser, PermissionsMixin):
    REGISTRATION_CHOICES = [
        ("local", "Local"),
        ("google", "Google"),
        ("facebook", "Facebook"),
    ]
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=20, null=True, blank=True)
    birthdate = models.DateField(null=True, blank=True)
    first_name = models.CharField(max_length=100, null=True, blank=True)
    last_name = models.CharField(max_length=100, null=True, blank=True)

    registration_source = models.CharField(
        max_length=20,
        default="local"
    )


    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['phone_number', 'birthdate']
    EMAIL_FIELD = 'email'

  #работает только в django admin
    def clean(self):
        super().clean()
        if self.is_superuser and not self.phone_number:
            raise ValidationError({
                "phone_number": "Номер телефона обязателен для суперпользователя"
            })


    def __str__(self) -> str:
        return self.email or ""






