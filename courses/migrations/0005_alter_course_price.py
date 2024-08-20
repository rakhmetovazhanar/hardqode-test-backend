# Generated by Django 4.2.10 on 2024-08-20 17:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0004_course_price_group_course_group_student_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='course',
            name='price',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=15, verbose_name='Стоимость'),
        ),
    ]
