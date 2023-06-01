# -*-coding:UTF-8-*-
"""
@Project : django_test
@File : shop.py
@IDE : PyCharm
@Author : 何顺昌
@Date : 2023/5/3015:11
"""

from drf_yasg.utils import swagger_auto_schema
from rest_framework import mixins, status
from rest_framework.decorators import action
from rest_framework.response import Response

from django_hrm.models import Shop
from django_hrm.prefetchers.shop import MyShopFetcher
from django_hrm.serializers import ShopSerializer
from django_hrm.serializers.shop import ShopCreateSerializer
from django_test.rest.filters import BaseFilterSet
from django_test.rest.viewsets import BaseGenericViewSet


class ShopFilterSet(BaseFilterSet):
    class Meta:
        model = Shop
        fields = {
            "business_id": ["exact"],
        }


class ShopViewSet(
    BaseGenericViewSet,
    mixins.CreateModelMixin
):
    queryset = Shop.objects.filter()
    serializer_class = ShopSerializer
    filterset_class = ShopFilterSet

    @swagger_auto_schema(
        request_body=ShopCreateSerializer(),
        responses={
            "200": "",
        },
        operation_description="商家创建店铺",
    )
    def create(self, request, *args, **kwargs):
        business = request.user.userprofile.business
        data = request.data
        data['business_id'] = business.id
        shop_serializer = ShopCreateSerializer(data=data)
        shop_serializer.is_valid(raise_exception=True)
        validated_data = shop_serializer.validated_data
        Shop.objects_internal.create(validated_data)
        return Response(status=status.HTTP_201_CREATED)

    @swagger_auto_schema(
        responses={
            "200": ShopSerializer(),
        },
        operation_description="我的店铺",
    )
    @action(methods=["get"], detail=False)
    def my_shop(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        queryset = queryset.filter(business_id=request.user.userprofile.business_id)
        person_list = MyShopFetcher(queryset, request).data
        return Response(person_list, status=status.HTTP_200_OK)
