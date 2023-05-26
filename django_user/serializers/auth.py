# -*- coding: utf-8 -*-
from rest_framework import serializers

from django_user.models import UserProfile
from django_user.serializers.base import BaseModelSerializer


class AuthSerializer(serializers.Serializer):
    username = serializers.CharField(required=True, allow_blank=False, max_length=100)
    password = serializers.CharField(required=True, allow_blank=False, max_length=100)
    token_max_age = serializers.IntegerField(min_value=1, max_value=60, default=1)


class AuthUserSerializer(serializers.ModelSerializer):
    class Meta(BaseModelSerializer.Meta):
        model = UserProfile
        fields = ('id', 'name', 'type', 'is_admin', "is_enabled")


class AuthResponseSerializer(serializers.Serializer):
    username = serializers.CharField(required=True, allow_blank=False, max_length=100)
    userprofile = AuthUserSerializer()
