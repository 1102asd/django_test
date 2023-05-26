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

from django_hrm.models import Customer, Business
from django_test.db.models import BaseModel, UnsignedBigAutoField


class AttentionLinkManager(models.Manager):
    @transaction.atomic
    def like(self, customer_id, business_id):
        customer = Customer.objects.filter(id=customer_id).first()
        customer.attention_count += 1
        customer.save()
        business = Business.objects.filter(id=business_id).first()
        business.be_attention_count += 1
        business.save()
        return business


class CustomerToBusiness():
    class Meta(BaseModel.Meta):
        db_table = "customer"

    class ForeignKeyConstraint:
        fields = {
            "create_user_id": {"to_model": "django_user.UserProfile"},
            "business_id": {"to_model": "django_hrm.Business"},
            "customer_id": {"to_model": "django_hrm.Customer"},
        }

    id = UnsignedBigAutoField(primary_key=True, editable=False)
    customer_id = UnsignedBigAutoField(verbose_name="顾客id", help_text="顾客id")
    business_id = UnsignedBigAutoField(verbose_name="关注商家id", help_text="关注商家id")

    # 关注时原子化信息
    objects_internal = AttentionLinkManager()
