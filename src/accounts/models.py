from django.db import models
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import UserManager


class MyUser(AbstractBaseUser):
    email = models.EmailField(
        verbose_name='email_addrees',
        max_length=30,
        unique=True
    )
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    city = models.ForeignKey(
        'City',
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    langiage = models.ForeignKey(
        'Language',
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    send_email = models.BooleanField(default=True)
    objects = UserManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self) -> str:
        return self.email

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app, label):
        return True

    @property
    def is_staff(self):
        return self.is_admin
