# -*-coding:UTF-8-*-
"""
@Project : django_test
@File : use.py
@IDE : PyCharm
@Author : 何顺昌
@Date : 2023/5/2517:52
"""
from django.conf import settings
from django.db import models
from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver
from django.contrib.auth.models import User

from django_hrm.models import Business, Customer
from django_test.db.models import UnsignedBigIntegerField
from django_user.models.base import BaseModel


class UserProfile(BaseModel):
    class Meta(BaseModel.Meta):
        db_table = 'user'

    class ForeignKeyConstraint:
        fields = {
            "create_user_id": {"to_model": "django_user.UserProfile"},
            "business_id": {"to_model": "django_hrm.Business"},
            "customer_id": {"to_model": "django_hrm.Customer"},
        }

    class UserType(models.IntegerChoices):
        ADMIN = 0, '管理员'
        CUSTOMER = 1, '顾客'
        BUSINESS = 2, '商家'

    user = models.OneToOneField(settings.AUTH_USER_MODEL, verbose_name="账号", on_delete=models.CASCADE)
    name = models.CharField(verbose_name="姓名", max_length=100, help_text="姓名", blank=True)
    type = models.SmallIntegerField(verbose_name='用户类型', choices=UserType.choices, default=UserType.CUSTOMER)
    business_id = UnsignedBigIntegerField(verbose_name="绑定商家 ID", help_text="绑定商家 ID", null=True)
    customer_id = UnsignedBigIntegerField(verbose_name="绑定顾客 ID", help_text="绑定顾客 ID", null=True)

    is_admin = models.BooleanField(verbose_name='是否是管理权限组成员', default=False)
    is_enabled = models.BooleanField(verbose_name='是否启用', default=True, help_text='是否启用，启用才可以登录')

    def _get_business(self):
        if not hasattr(self, '_business'):
            self._business = None
            if self.business_id:
                self._business = Business.objects.get(id=self.business_id)
        return self._business

    def _set_business(self, business):
        self._business = business

    def _get_customer(self):
        if not hasattr(self, '_customer'):
            self._customer = None
            if self.customer_id:
                self._business = Customer.objects.get(id=self.customer_id)
        return self._customer

    def _set_customer(self, customer):
        self._customer = customer

    customer = property(_get_customer, _set_customer)
    business = property(_get_business, _set_business)
    del _get_customer, _set_customer
    del _set_business, _get_business

    def __unicode__(self):
        return "用户: {}".format(self.name)


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, using, **kwargs):
    if created:
        try:
            UserProfile.objects.using(using).get(user=instance)
        except UserProfile.DoesNotExist:
            UserProfile.objects.using(using).create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, using, **kwargs):
    instance.userprofile.save(using=using)
