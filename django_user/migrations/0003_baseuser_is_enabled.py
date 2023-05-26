# Generated by Django 3.0.14 on 2023-05-26 11:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('django_user', '0002_baseuser_is_admin'),
    ]

    operations = [
        migrations.AddField(
            model_name='baseuser',
            name='is_enabled',
            field=models.BooleanField(default=True, help_text='是否启用，启用才可以登录', verbose_name='是否启用'),
        ),
    ]
