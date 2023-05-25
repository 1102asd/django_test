# -*-coding:UTF-8-*-
"""
@Project : django_test
@File : use.py
@IDE : PyCharm
@Author : 何顺昌
@Date : 2023/5/2518:10
"""
from drf_yasg.utils import swagger_auto_schema
from rest_framework import mixins

from django_test.rest.viewsets import BaseGenericViewSet
from django_user.models import BaseUser


class UserViewSet(
    BaseGenericViewSet,
    mixins.ListModelMixin,
):
    """
    问诊记录
    """

    queryset = BaseUser.objects.filter().order_by("-create_time")
    serializer_class = RecodingListSerializer
    filterset_class = InquiryRecodingFilterSet

    @swagger_auto_schema(
        responses={
            "200": RecodingListSerializer(many=True),
        },
        operation_description="我的问诊记录",
    )
    def list(self, request, *args, **kwargs):
        user_id = get_current_user_id(request)
        queryset = self.get_queryset()