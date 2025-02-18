from django.contrib.auth.models import AbstractUser
from django.db import models
from rest_framework import permissions
from rest_framework.decorators import action
from django.apps import apps


class CustomUser(AbstractUser):
    """Кастомная модель пользователя - студента."""

    email = models.EmailField(
        verbose_name='Адрес электронной почты',
        max_length=250,
        unique=True
    )
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = (
        'username',
        'first_name',
        'last_name',
        'password'
    )

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ('-id',)

    def __str__(self):
        return self.get_full_name()


class Balance(models.Model):
    """Модель баланса пользователя."""

    # TODO
    user = models.OneToOneField(
        CustomUser,
        on_delete=models.CASCADE,
        default=None,
        verbose_name='Студент'
    )
    balance = models.PositiveIntegerField(
        default=1000,
        verbose_name='Баланс'
    )

    @action(permission_classes=permissions.IsAdminUser,
            detail=True)
    def add_balance(self, balance):
        self.balance += balance

    class Meta:
        verbose_name = 'Баланс'
        verbose_name_plural = 'Балансы'
        ordering = ('-id',)


class Subscription(models.Model):
    """Модель подписки пользователя на курс."""

    # TODO
    #Course = apps.get_model('courses', 'Course')
    user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        verbose_name='Пользователь',
        default=None
    )

    course = models.ForeignKey(
        'courses.Course',
        on_delete=models.CASCADE,
        verbose_name='Курс',
        default=None)

    class Meta:
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'
        ordering = ('-id',)

