# -*-coding:UTF-8-*-
"""
@Project : django_test
@File : attentionlink.py
@IDE : PyCharm
@Author : 何顺昌
@Date : 2023/5/3014:24
"""
from django_test.utils.model_extra_fields import ModelExtraFieldsBase


class CustomerListFetcher(ModelExtraFieldsBase):
    def __init__(self, objs, request):
        self.request = request
        mappings = {
            "id": ["self", "id"],
            "create_time": ["self", "create_time"],
            "update_time": ["self", "update_time"],
            "business_id": ["self", "business_id"],
            "business_name": ["business", "name"],
            # "business_tag": ['business']
        }
        super(CustomerListFetcher, self).__init__(mappings, objs)
