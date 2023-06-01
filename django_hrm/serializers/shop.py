# -*-coding:UTF-8-*-
"""
@Project : django_test
@File : shop.py
@IDE : PyCharm
@Author : 何顺昌
@Date : 2023/5/3015:12
"""
from rest_framework import serializers

from django_hrm.models import Shop, Business, ShopStyle
from django_test.utils.rest_serializers import BaseModelSerializer


class ShopSerializer(BaseModelSerializer):
    class Meta(BaseModelSerializer.Meta):
        model = Shop


class ShopExistsValidator(object):
    def __call__(self, value):
        if Shop.objects.filter(shop_name=value).first():
            message = '此店铺名称： %s - 存在' % value
            raise serializers.ValidationError(message)


class BusinessExistsValidator(object):
    def __call__(self, value):
        if not Business.objects.get(id=value):
            message = '此商家： %s - 不存在' % value
            raise serializers.ValidationError(message)


class ShopCreateSerializer(serializers.Serializer):
    shop_name = serializers.CharField(help_text="店铺名称", max_length=128, validators=[ShopExistsValidator()])
    shop_url = serializers.CharField(help_text="店铺url", max_length=128)
    shop_pic = serializers.CharField(help_text="店铺图片url", max_length=128)
    content = serializers.CharField(help_text="店铺简介", required=False)
    business_id = serializers.IntegerField(help_text="所属商家Id")
    tag_ids = serializers.ListSerializer(help_text="类型Id列表", child=serializers.IntegerField())

    def validate_business_id(self, value):
        if not Business.objects.get(id=value):
            message = '此商家： %s - 不存在' % value
            raise serializers.ValidationError(message)
        return value

    def validate_tag_ids(self, value):
        for tag_id in value:
            if not ShopStyle.objects.get(id=tag_id):
                message = '此商家种类id： %s - 不存在' % tag_id
                raise serializers.ValidationError(message)
        return value
