# -*-coding:UTF-8-*-
"""
@Project : django_test
@File : shop.py
@IDE : PyCharm
@Author : 何顺昌
@Date : 2023/5/2615:21
"""

from django_test.db.models import BaseModel, UnsignedBigAutoField, UnsignedBigIntegerField
from django.db import models, transaction


class ShopManager(models.Manager):
    @transaction.atomic
    def create(self, data):
        from django_hrm.models import ShopToStyle
        shop_obj = Shop.objects.filter(shop_name=data.get("shop_name")).first()
        if not shop_obj:
            shop_data = {
                "shop_name": data.get("shop_name"),
                "shop_url": data.get("shop_url"),
                "shop_pic": data.get("shop_pic"),
                "content": data.get("content"),
                "business_id": data.get("business_id"),
            }
            shop_obj = Shop.objects.create(**shop_data)
        tag_ids = data.get('tag_ids')
        for tag_id in tag_ids:
            tag_data = {
                "shop_id": shop_obj.id,
                "shop_style_id": tag_id,
                "business_id": shop_obj.business_id,
            }
            ShopToStyle.objects.get_or_create(**tag_data)
        return True


class Shop(BaseModel):
    class Meta(BaseModel.Meta):
        db_table = "business_shop"

    class ForeignKeyConstraint:
        fields = {
            "create_user_id": {"to_model": "django_user.UserProfile"},
            "business_id": {"to_model": "django_hrm.Business"},
        }

    id = UnsignedBigAutoField(primary_key=True, editable=False)
    shop_name = models.CharField(verbose_name="店铺名称", help_text="店铺名称", max_length=128)
    shop_url = models.CharField(verbose_name="店铺url", help_text="店铺url", max_length=128)
    shop_pic = models.CharField(verbose_name="店铺图片url", help_text="店铺图片url", max_length=128)
    content = models.TextField(verbose_name="店铺简介", help_text="店铺简介", null=True)
    business_id = UnsignedBigIntegerField(verbose_name="所属商家Id", help_text="所属商家Id")

    # 关注时原子化信息
    objects_internal = ShopManager()
