from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser
import pycountry

class CustomUserManager(BaseUserManager):
    def create_user(self, first_name, last_name, username, email, password=None, country="Egypt", phone_number=None):
        if not email:
            raise ValueError('The Email field must be set')
        if not username:
            raise ValueError('The Username field must be set')

        user = self.model(
            email=self.normalize_email(email),
            first_name=first_name,
            last_name=last_name,
            username=username,
            country=country,
            phone_number=phone_number
        )
        user.set_password(password)
        user.is_active = False  # لتفعيل الحساب فورًا
        user.save(using=self._db)
        return user

    def create_superuser(self, first_name, last_name, username, email, password=None, country="Egypt", phone_number=None):
        user = self.create_user(
            email=email,
            first_name=first_name,
            last_name=last_name,
            username=username,
            password=password,
            country=country,
            phone_number=phone_number
        )
        user.is_admin = True
        user.is_staff = True
        user.is_superadmin = True
        user.is_active = True
        user.save(using=self._db)
        return user


class Account(AbstractBaseUser):
    first_name      = models.CharField(max_length=50)
    last_name       = models.CharField(max_length=50)
    username        = models.CharField(max_length=50, unique=True)
    email           = models.EmailField(max_length=100, unique=True)
    country         = models.CharField(
        max_length=100,
        choices=[(c.name, c.name) for c in pycountry.countries],
        default="Egypt"
    )
    phone_number    = models.CharField(max_length=15, blank=True, null=True)

    date_joined     = models.DateTimeField(auto_now_add=True)
    last_login      = models.DateTimeField(auto_now=True)
    is_admin        = models.BooleanField(default=False)
    is_staff        = models.BooleanField(default=False)
    is_active       = models.BooleanField(default=True)
    is_superadmin   = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    objects = CustomUserManager()

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return True
