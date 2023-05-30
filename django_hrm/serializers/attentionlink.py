# -*-coding:UTF-8-*-
"""
@Project : django_test
@File : attentionlink.py
@IDE : PyCharm
@Author : 何顺昌
@Date : 2023/5/3013:45
"""
from rest_framework import serializers

from django_hrm.models import AttentionLink
from django_test.utils.rest_serializers import BaseModelSerializer


class AttentionLinkSerializer(BaseModelSerializer):
    customer_id = serializers.IntegerField(required=False)

    class Meta(BaseModelSerializer.Meta):
        model = AttentionLink
