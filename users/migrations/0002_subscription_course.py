# Generated by Django 4.2.10 on 2024-08-18 20:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0002_lesson_course'),
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='subscription',
            name='course',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='courses.course', verbose_name='Курс'),
        ),
    ]
