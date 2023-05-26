# -*-coding:UTF-8-*-
"""
@Project : django_test
@File : customer.py
@IDE : PyCharm
@Author : 何顺昌
@Date : 2023/5/2615:33
"""
from django.db import models

from django_test.db.models import BaseModel, UnsignedBigAutoField, UnsignedIntegerField


class Customer(BaseModel):
    class Meta(BaseModel.Meta):
        db_table = "customer"

    class ForeignKeyConstraint:
        fields = {
            "create_user_id": {"to_model": "django_user.UserProfile"},
        }

    id = UnsignedBigAutoField(primary_key=True, editable=False)
    name = models.CharField(verbose_name="顾客账户名称", help_text="商家账户名称")
    customer_url = models.CharField(verbose_name="顾客头像url", help_text="顾客头像url")
    context = models.TextField(verbose_name="顾客简介", help_text="顾客简介")
    attention_count = UnsignedIntegerField(verbose_name='关注的店铺数量', default=0)
