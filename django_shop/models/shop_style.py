# -*-coding:UTF-8-*-
"""
@Project : django_test
@File : shop_style.py
@IDE : PyCharm
@Author : 何顺昌
@Date : 2023/5/2615:26
"""
from django_test.db.models import BaseModel, UnsignedBigAutoField
from django.db import models


class ShopStyle(BaseModel):
    class Meta(BaseModel.Meta):
        db_table = "shop_style"

    class ForeignKeyConstraint:
        fields = {
            "create_user_id": {"to_model": "django_user.UserProfile"},
        }

    id = UnsignedBigAutoField(primary_key=True, editable=False)
    tag_name = models.CharField(verbose_name="店铺类型", )


class ShopToStyle(BaseModel):
    class Meta(BaseModel.Meta):
        db_table = "shop_to_style"

    class ForeignKeyConstraint:
        fields = {
            "create_user_id": {"to_model": "django_user.UserProfile"},
            "shop_style_id": {"to_model": "django_shop.ShopStyle"},
            "shop_id": {"to_model": "django_shop.Shop"},
        }

    id = UnsignedBigAutoField(primary_key=True, editable=False)
    shop_id = UnsignedBigAutoField(verbose_name="店铺id")
    shop_style_id = UnsignedBigAutoField(verbose_name="店铺类型id")
