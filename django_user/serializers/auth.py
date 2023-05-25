# -*- coding: utf-8 -*-
from rest_framework import serializers


class AuthSerializer(serializers.Serializer):
    username = serializers.CharField(required=True, allow_blank=False, max_length=100)
    password = serializers.CharField(required=True, allow_blank=False, max_length=100)
    token_max_age = serializers.IntegerField(min_value=1, max_value=60, default=1)
