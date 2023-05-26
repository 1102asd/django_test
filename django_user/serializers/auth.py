# -*- coding: utf-8 -*-
from rest_framework import serializers
from django_user.serializers import UserSerializer


class AuthSerializer(serializers.Serializer):
    username = serializers.CharField(required=True, allow_blank=False, max_length=100)
    password = serializers.CharField(required=True, allow_blank=False, max_length=100)
    token_max_age = serializers.IntegerField(min_value=1, max_value=60, default=1)


class AuthResponseSerializer(serializers.Serializer):
    token = serializers.CharField()
    expires = serializers.DateTimeField()
    userprofile = UserSerializer()
