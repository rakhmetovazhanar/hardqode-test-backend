# Generated by Django 4.2.10 on 2024-08-18 20:42

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_balance_balance_balance_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='balance',
            name='user',
            field=models.OneToOneField(default=None, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Студент'),
        ),
    ]
