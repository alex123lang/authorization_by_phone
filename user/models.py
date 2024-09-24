from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.utils import timezone


class UserManager(BaseUserManager):
    """
    Менеджер для пользователей.
    """
    def create_user(self, email, username, password=None, **extra_fields):
        """Создает и возвращает пользователя с email и паролем"""
        if not email:
            raise ValueError('У пользователя должен быть email адрес')
        email = self.normalize_email(email)
        user = self.model(email=email, username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password=None, **extra_fields):
        """Создает и возвращает суперпользователя"""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Суперпользователь должен иметь is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Суперпользователь должен иметь is_superuser=True.')

        return self.create_user(email, username, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    """
    Модель пользователя.
    """
    email = models.EmailField(unique=True, verbose_name='Email')
    username = models.CharField(max_length=255, unique=True, verbose_name='Имя пользователя')
    is_active = models.BooleanField(default=True, verbose_name='Активен')
    is_staff = models.BooleanField(default=False, verbose_name='Сотрудник')
    date_joined = models.DateTimeField(default=timezone.now, verbose_name='Дата регистрации')

    objects = UserManager()

    USERNAME_FIELD = 'email'  # Для входа используем email
    REQUIRED_FIELDS = ['username']  # Поля, которые обязательны при создании суперпользователя

    def __str__(self):
        return self.email
