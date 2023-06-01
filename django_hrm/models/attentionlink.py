# -*-coding:UTF-8-*-
"""
@Project : django_test
@File : customer_to_business.py
@IDE : PyCharm
@Author : 何顺昌
@Date : 2023/5/2615:40
"""
from django.db import transaction
from django.db import models

from django_test.db.models import BaseModel, UnsignedBigAutoField, UnsignedBigIntegerField


class AttentionLinkManager(models.Manager):
    @transaction.atomic
    def like(self, customer_id, shop_id):
        from django_hrm.models import Customer, Shop
        attention_obj = AttentionLink.objects.filter(customer_id=customer_id, shop_id=shop_id).first()
        if not attention_obj:
            customer = Customer.objects.filter(id=customer_id).first()
            customer.attention_count += 1
            customer.save()
            shop = Shop.objects.filter(id=shop_id).first()
            shop.be_attention_count += 1
            shop.save()
            AttentionLink.objects.create(customer_id=customer_id, shop_id=shop_id)


class AttentionLink(BaseModel):
    class Meta(BaseModel.Meta):
        db_table = "customer_attention_link"

    class ForeignKeyConstraint:
        fields = {
            "create_user_id": {"to_model": "django_user.UserProfile"},
            "shop_id": {"to_model": "django_hrm.Shop"},
            "customer_id": {"to_model": "django_hrm.Customer"},
        }

    id = UnsignedBigAutoField(primary_key=True, editable=False)
    customer_id = UnsignedBigIntegerField(verbose_name="顾客id", help_text="顾客id")
    shop_id = UnsignedBigIntegerField(verbose_name="关注商家的店铺ID", help_text="关注商家的店铺ID")

    # 关注时原子化信息
    objects_internal = AttentionLinkManager()
