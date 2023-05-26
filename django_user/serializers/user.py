# -*- coding: utf-8 -*-
from django.contrib.auth.models import User
from django.contrib.auth.validators import ASCIIUsernameValidator

from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from .base import BaseModelSerializer
from ..models.user import BaseUser


class UserProfileSerializer(BaseModelSerializer):
    name = serializers.CharField(max_length=128, help_text="用户名", required=True, allow_blank=False, )
    type = serializers.ChoiceField(
        choices=BaseUser.UserType.choices, help_text="类别"
    )

    class Meta(BaseModelSerializer.Meta):
        model = BaseUser
        exclude = ['user', 'created', 'updated']
        read_only_fields = ['is_admin']


class UserSerializer(serializers.ModelSerializer):
    username = serializers.CharField(max_length=20, min_length=2, validators=[
        ASCIIUsernameValidator(),
        UniqueValidator(queryset=User.objects.all())
    ])
    password = serializers.CharField(max_length=18, min_length=6)
    type = serializers.ChoiceField(
        choices=BaseUser.UserType.choices, help_text="类别"
    )
    baseuser = UserProfileSerializer()

    class Meta(BaseModelSerializer.Meta):
        model = User
        fields = ('id', 'username', 'password', 'type', 'baseuser')

    def create(self, validated_data):
        type = validated_data.pop("type")
        user = User.objects.create_user(**validated_data)
        setattr(user.baseuser, "type", type)
        setattr(user.baseuser, "name", validated_data['username'])
        user.baseuser.save()
        user.save()
        return user
