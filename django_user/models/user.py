# -*-coding:UTF-8-*-
"""
@Project : django_test
@File : use.py
@IDE : PyCharm
@Author : 何顺昌
@Date : 2023/5/2517:52
"""
from django.conf import settings
from django.db import models
from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver
from django.contrib.auth.models import User

from django_user.models.base import BaseModel


class UserProfile(BaseModel):
    class Meta(BaseModel.Meta):
        db_table = 'user'

    class UserType(models.IntegerChoices):
        ADMIN = 0, '管理员'
        CUSTOMER = 1, '普通用户'
        VIP_CUSTOMER = 2, 'VIP'

    user = models.OneToOneField(settings.AUTH_USER_MODEL, verbose_name="账号", on_delete=models.CASCADE)
    name = models.CharField(verbose_name="姓名", max_length=100, help_text="姓名", blank=True)
    type = models.SmallIntegerField(verbose_name='用户类型', choices=UserType.choices, default=UserType.CUSTOMER)
    is_admin = models.BooleanField(verbose_name='是否是管理权限组成员', default=False)
    is_enabled = models.BooleanField(verbose_name='是否启用', default=True, help_text='是否启用，启用才可以登录')


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, using, **kwargs):
    if created:
        try:
            UserProfile.objects.using(using).get(user=instance)
        except UserProfile.DoesNotExist:
            UserProfile.objects.using(using).create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, using, **kwargs):
    instance.userprofile.save(using=using)
