# -*-coding:UTF-8-*-
"""
@Project : django_test
@File : shop.py
@IDE : PyCharm
@Author : 何顺昌
@Date : 2023/5/2615:13
"""
from django_test.db.models import BaseModel, UnsignedBigAutoField
from django.db import models


class Commodity(BaseModel):
    class Meta(BaseModel.Meta):
        db_table = "commodity"

    id = UnsignedBigAutoField(primary_key=True, editable=False)
    commodity_name = models.CharField(verbose_name='商品名称', max_length=128)
    is_sales = models.BooleanField(verbose_name='是否还在售卖', default=True)
    score = models.FloatField(default=0, help_text="业绩分-积分制, +10为加10分，-10为减10分")
    price = models.FloatField(default=0, help_text="商品价格")
    context = models.TextField(verbose_name='商品介绍', help_text='商品介绍', null=True)
    commodity_url = models.CharField(verbose_name='商品地址', help_text="商品地址",max_length=128)
