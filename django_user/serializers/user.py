# -*- coding: utf-8 -*-
from django.contrib.auth.models import User
from django.contrib.auth.validators import ASCIIUsernameValidator

from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from django_hrm.models import Customer, Business
from django_hrm.serializers.business import BusinessSerializer
from django_hrm.serializers.customer import CustomerSerializer
from django_user.models import UserProfile
from django_user.serializers import BaseModelSerializer


class CustomerExistsValidator(object):
    def __call__(self, value):
        if not Customer.objects.get(id=value):
            message = '无效人员 %s - 这个人员 ID 不存在' % value
            raise serializers.ValidationError(message)


class BusinessExistsValidator(object):
    def __call__(self, value):
        if not Business.objects.get(id=value):
            message = '无效人员 %s - 这个人员 ID 不存在' % value
            raise serializers.ValidationError(message)


class UserProfileSerializer(BaseModelSerializer):
    customer_id = serializers.CharField(max_length=128, help_text="绑定顾客 ID", required=True, allow_blank=False,
                                        validators=[CustomerExistsValidator()])

    # business_id = serializers.CharField(max_length=128, help_text="绑定商家 ID", required=True, allow_blank=False,
    #                                     validators=[BusinessExistsValidator()])
    customer = CustomerSerializer(read_only=True)
    business = BusinessSerializer(read_only=True)

    class Meta(BaseModelSerializer.Meta):
        model = UserProfile
        exclude = ['user', 'created', 'updated']
        read_only_fields = ['is_admin', 'customer', 'business', "type"]


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
        choices=UserProfile.UserType.choices, help_text="类别", required=False
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


class UserPasswordSerializer(serializers.Serializer):
    password = serializers.CharField(max_length=18, min_length=6)
