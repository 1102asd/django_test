# -*-coding:UTF-8-*-
"""
@Project : django_test
@File : shop_style.py
@IDE : PyCharm
@Author : 何顺昌
@Date : 2023/5/3014:46
"""
from drf_yasg.utils import swagger_auto_schema
from rest_framework import mixins, status
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response

from django_hrm.models import ShopStyle
from django_test.exceptions import UserPermissionError
from django_test.rest.filters import BaseFilterSet
from django_test.rest.viewsets import BaseGenericViewSet
from django_user.serializers import ShopStyleSerializer


class ShopStyleFilterSet(BaseFilterSet):
    class Meta:
        model = ShopStyle
        fields = {
            "tag_name": ["exact"],
        }


class ShopStyleViewSet(
    BaseGenericViewSet,
    mixins.ListModelMixin,
    mixins.CreateModelMixin
):
    queryset = ShopStyle.objects.filter()
    serializer_class = ShopStyleSerializer
    filterset_class = ShopStyleFilterSet

    @swagger_auto_schema(
        request_body=ShopStyleSerializer(),
        responses={
            "200": ShopStyleSerializer(),
        },
        operation_description="创建商品种类",
    )
    def create(self, request, *args, **kwargs):
        if request.user.userprofile.is_admin:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        else:
            raise UserPermissionError()

    @swagger_auto_schema(
        responses={
            "200": ShopStyleSerializer(),
        },
        operation_description="商品种类列表",
    )
    def list(self, request, *args, **kwargs):
        return super(ShopStyleViewSet, self).list(request, *args, **kwargs)
