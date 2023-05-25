# -*-coding:UTF-8-*-
"""
@Project : django_test
@File : use.py
@IDE : PyCharm
@Author : 何顺昌
@Date : 2023/5/2517:52
"""
from django.db import models

from django_user.models.base import BaseModel


class BaseUser(BaseModel):
    class Meta(BaseModel.Meta):
        db_table = 'user'

    class UserType(models.IntegerChoices):
        ADMIN = 0, '管理员'
        CUSTOMER = 1, '普通用户'
        VIP_CUSTOMER = 2, 'VIP'

    name = models.CharField(verbose_name="姓名", max_length=100, help_text="姓名", blank=True)
    type = models.SmallIntegerField(verbose_name='用户类型', choices=UserType.choices, default=UserType.CUSTOMER)
    passwd = models.CharField(verbose_name="密码", max_length=100, help_text="密码", blank=True)
