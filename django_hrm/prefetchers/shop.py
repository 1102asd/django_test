# -*-coding:UTF-8-*-
"""
@Project : django_test
@File : shop.py
@IDE : PyCharm
@Author : 何顺昌
@Date : 2023/6/113:56
"""
from django_test.utils.model_extra_fields import ModelExtraFieldsBase
from django_user.models import UserProfile


class MyShopFetcher(ModelExtraFieldsBase):
    def __init__(self, objs, request):
        self.request = request
        mappings = {
            "id": ["self", "id"],
            "create_time": ["self", "create_time"],
            "update_time": ["self", "update_time"],
            "business_id": ["self", "business_id"],
            "be_attention_count": ["self", "be_attention_count"],
            "business_name": ["business", "name"],
            "shop_name": ["self", "shop_name"],
            "shop_url": ["self", "shop_url"],
            "shop_pic": ["self", "shop_pic"],
            "content": ["self", "content"],
            "tags": ["shoptostyle_set__shop_style", self._get_tag],
            # "business_tag": ['business']
        }
        super(MyShopFetcher, self).__init__(mappings, objs)

    def _get_tag(self, instance):
        tag_list = []
        if self.request.user.type == UserProfile.UserType.BUSINESS:
            shop_tag_list = instance.shoptostyle_set
            for shop_tag_obj in shop_tag_list:
                tag_name = shop_tag_obj.shop_style.tag_name
                tag_list.append(tag_name)
        return tag_list
