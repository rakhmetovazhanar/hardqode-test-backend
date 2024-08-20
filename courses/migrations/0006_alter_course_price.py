# Generated by Django 4.2.10 on 2024-08-20 17:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0005_alter_course_price'),
    ]

    operations = [
        migrations.AlterField(
            model_name='course',
            name='price',
            field=models.DecimalField(decimal_places=2, default='d', max_digits=15, verbose_name='Стоимость'),
        ),
    ]
