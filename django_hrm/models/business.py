# -*-coding:UTF-8-*-
"""
@Project : django_test
@File : business.py
@IDE : PyCharm
@Author : 何顺昌
@Date : 2023/5/2615:36
"""
from django.db import models

from django_test.db.models import BaseModel, UnsignedBigAutoField, UnsignedIntegerField


class Business(BaseModel):
    class Meta(BaseModel.Meta):
        db_table = "business"

    class ForeignKeyConstraint:
        fields = {
            "create_user_id": {"to_model": "django_user.UserProfile"},
        }

    id = UnsignedBigAutoField(primary_key=True, editable=False)
    name = models.CharField(verbose_name="商家账户名称", help_text="商家账户名称")
    business_url = models.CharField(verbose_name="商家头像url", help_text="商家头像url")
    context = models.TextField(verbose_name="商家简介", help_text="商家简介")
    be_attention_count = UnsignedIntegerField(verbose_name='被多少顾客关注', default=0)
