# -*-coding:UTF-8-*-
"""
@Project : django_test
@File : shop_style.py
@IDE : PyCharm
@Author : 何顺昌
@Date : 2023/5/3014:47
"""
from django_hrm.models import ShopStyle
from django_test.utils.rest_serializers import BaseModelSerializer


class ShopStyleSerializer(BaseModelSerializer):
    class Meta(BaseModelSerializer.Meta):
        model = ShopStyle
