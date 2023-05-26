# -*- coding: utf-8 -*-
from django.contrib.auth.models import User
from django.contrib.auth.validators import ASCIIUsernameValidator

from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from .base import BaseModelSerializer
from ..models.user import UserProfile


class UserProfileSerializer(BaseModelSerializer):
    name = serializers.CharField(max_length=128, help_text="用户名", required=True, allow_blank=False, )
    type = serializers.ChoiceField(
        choices=UserProfile.UserType.choices, help_text="类别"
    )
    is_admin = serializers.BooleanField(label="是否是admin用户", default=False, required=False)

    class Meta(BaseModelSerializer.Meta):
        model = UserProfile
        exclude = ['user', 'created', 'updated']
        read_only_fields = ['is_admin']

    def validate_is_admin(self, value):
        if self.type == UserProfile.UserType.ADMIN:
            return True
        return False


class UserPostSerializer(serializers.ModelSerializer):
    username = serializers.CharField(max_length=20, min_length=2, validators=[
        ASCIIUsernameValidator(),
        UniqueValidator(queryset=User.objects.all())
    ])
    password = serializers.CharField(max_length=18, min_length=6)
    type = serializers.ChoiceField(
        choices=UserProfile.UserType.choices, help_text="类别"
    )

    class Meta(BaseModelSerializer.Meta):
        model = User
        fields = ('id', 'username', 'password', 'type')


class UserSerializer(serializers.ModelSerializer):
    username = serializers.CharField(max_length=20, min_length=2, validators=[
        ASCIIUsernameValidator(),
        UniqueValidator(queryset=User.objects.all())
    ])
    password = serializers.CharField(max_length=18, min_length=6)
    type = serializers.ChoiceField(
        choices=UserProfile.UserType.choices, help_text="类别"
    )
    userprofile = UserProfileSerializer()

    class Meta(BaseModelSerializer.Meta):
        model = User
        fields = ('id', 'username', 'password', 'type', 'userprofile')

    def create(self, validated_data):
        type = validated_data.pop("type")
        user = User.objects.create_user(**validated_data)
        setattr(user.userprofile, "type", type)
        setattr(user.userprofile, "name", validated_data['username'])
        if type == UserProfile.UserType.ADMIN:
            setattr(user.userprofile, "is_admin", True)
        else:
            setattr(user.userprofile, "is_admin", False)
        user.userprofile.save()
        user.save()
        return user
