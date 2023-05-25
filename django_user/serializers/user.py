# -*- coding: utf-8 -*-
from django.contrib.auth.models import User
from django.contrib.auth.validators import ASCIIUsernameValidator

from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from .base import BaseModelSerializer
from ..models.user import BaseUser


class UserSerializer(serializers.ModelSerializer):
    username = serializers.CharField(max_length=20, min_length=2, validators=[
        ASCIIUsernameValidator(),
        UniqueValidator(queryset=User.objects.all())
    ])
    password = serializers.CharField(max_length=18, min_length=6, write_only=True)
    type = serializers.ChoiceField(
        choices=BaseUser.UserType.choices, help_text="类别"
    )
    class Meta(BaseModelSerializer.Meta):
        model = User
        fields = ('id', 'username', 'password', 'userprofile')
