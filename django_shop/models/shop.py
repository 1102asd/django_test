# -*-coding:UTF-8-*-
"""
@Project : django_test
@File : shop.py
@IDE : PyCharm
@Author : 何顺昌
@Date : 2023/5/2615:21
"""
from django_test.db.models import BaseModel, UnsignedBigAutoField
from django.db import models


class Shop(BaseModel):
    class Meta(BaseModel.Meta):
        db_table = "shop"

    class ForeignKeyConstraint:
        fields = {
            "create_user_id": {"to_model": "django_user.UserProfile"},
        }

    id = UnsignedBigAutoField(primary_key=True, editable=False)
    shop_name = models.CharField(verbose_name="店铺名称", help_text="店铺名称", max_length=128)
    shop_url = models.CharField(verbose_name="店铺url", help_text="店铺url", max_length=128)
    shop_pic = models.CharField(verbose_name="店铺图片url", help_text="店铺图片url", max_length=128)
    content = models.TextField(verbose_name="店铺简介", help_text="店铺简介", null=True)
