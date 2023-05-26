# -*-coding:UTF-8-*-
"""
@Project : django_test
@File : customer.py
@IDE : PyCharm
@Author : 何顺昌
@Date : 2023/5/2616:16
"""
from rest_framework import serializers

from django_hrm.models import Customer
from django_user.serializers import BaseModelSerializer


class CreateCustomerSerializer(serializers.Serializer):
    username = serializers.CharField(required=True, allow_blank=False, max_length=100)
    password = serializers.CharField(required=True, allow_blank=False, max_length=100)
    token_max_age = serializers.IntegerField(min_value=1, max_value=60, default=1)

class CustomerSerializer(BaseModelSerializer):

    class Meta(BaseModelSerializer.Meta):
        model = Customer
