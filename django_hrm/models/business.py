# -*-coding:UTF-8-*-
"""
@Project : django_test
@File : business.py
@IDE : PyCharm
@Author : 何顺昌
@Date : 2023/5/2615:36
"""
import logging

from django.contrib.auth.models import User
from django.db import models, transaction

from django_test.db.models import BaseModel, UnsignedBigAutoField, UnsignedIntegerField


class Business(BaseModel):
    class Meta(BaseModel.Meta):
        db_table = "business"

    class ForeignKeyConstraint:
        fields = {
            "create_user_id": {"to_model": "django_user.UserProfile"},
        }

    id = UnsignedBigAutoField(primary_key=True, editable=False)
    name = models.CharField(verbose_name="商家账户名称", help_text="商家账户名称", max_length=128)
    business_url = models.CharField(verbose_name="商家头像url", help_text="商家头像url", max_length=128, null=True)
    context = models.TextField(verbose_name="商家简介", help_text="商家简介", null=True)
    be_attention_count = UnsignedIntegerField(verbose_name='被多少顾客关注', default=0)

    @classmethod
    def login(cls, user_name, password):
        from django_user.models import UserProfile, ApiToken
        user = User.objects.filter(username=user_name).first()
        if not user:
            with transaction.atomic():
                business_obj = cls.objects.create(name=user_name)

                user = User.objects.create_user(username=user_name, password=password)
                user.userprofile.type = UserProfile.UserType.CUSTOMER
                user.userprofile.name = user_name
                user.userprofile.business_id = business_obj.id
                business_obj.create_user_id = user.userprofile.id
                business_obj.update_user_id = user.userprofile.id
                business_obj.save()
                user.userprofile.save()
        logging.info('登录顾客用户id为', user.id)
        logging.info('user_profile的id为', user.userprofile.id)
        # 生成token
        token_obj, _ = ApiToken.objects.get_or_create(user=user)
        if token_obj.is_expired():
            token_obj.delete()
            token_obj, _ = ApiToken.objects.get_or_create(user=user)
        return token_obj, user
