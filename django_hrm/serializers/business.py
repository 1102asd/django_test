# -*-coding:UTF-8-*-
"""
@Project : django_test
@File : business.py
@IDE : PyCharm
@Author : 何顺昌
@Date : 2023/5/2616:52
"""
from django_hrm.models import Business
from django_test.utils.rest_serializers import (
    BaseModelSerializer,
)

class BusinessSerializer(BaseModelSerializer):
    class Meta(BaseModelSerializer.Meta):
        model = Business
