from asyncio import get_event_loop

from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, AbstractUser
from django.db import models

from helpers import add_contact


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError("The Email must be set")

        if "username" not in extra_fields:
            extra_fields["username"] = email

        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)

        user.bitrix_id = add_contact(user.first_name, user.last_name, user.email)
        user.save()

        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields["is_staff"] = True
        extra_fields["is_superuser"] = True
        extra_fields["is_active"] = True
        return self.create_user(email, password, **extra_fields)


class CustomUser(AbstractUser):
    bitrix_id = models.PositiveIntegerField("ID в Bitrix", blank=True, null=True)

    objects = CustomUserManager()

    def __str__(self):
        return self.username
