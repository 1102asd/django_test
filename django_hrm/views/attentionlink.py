# -*-coding:UTF-8-*-
"""
@Project : django_test
@File : attentionlink.py
@IDE : PyCharm
@Author : 何顺昌
@Date : 2023/5/3013:42
"""
from drf_yasg.utils import swagger_auto_schema
from rest_framework import mixins, status
from rest_framework.decorators import action
from rest_framework.response import Response

from django_hrm.models import AttentionLink
from django_hrm.prefetchers.attentionlink import CustomerListFetcher
from django_hrm.serializers.attentionlink import AttentionLinkSerializer
from django_test.rest.filters import BaseFilterSet
from django_test.rest.viewsets import BaseGenericViewSet
from django_test.utils.tools import get_current_user_id


class AttentionLinkFilterSet(BaseFilterSet):
    class Meta:
        model = AttentionLink
        fields = {
            "customer_id": ["exact"],
        }


class AttentionLinkViewSet(
    BaseGenericViewSet,
    mixins.CreateModelMixin
):
    queryset = AttentionLink.objects.filter()
    serializer_class = AttentionLinkSerializer
    filterset_class = AttentionLinkFilterSet

    @swagger_auto_schema(
        request_body=AttentionLinkSerializer(),
        responses={
            "200": "",
        },
        operation_description="顾客关注商家店铺",
    )
    def create(self, request, *args, **kwargs):
        customer = request.user.userprofile.customer
        attention_serializer = AttentionLinkSerializer(data=request.data)
        attention_serializer.is_valid(raise_exception=True)
        validated_data = attention_serializer.validated_data
        AttentionLink.objects_internal.like(customer.id, validated_data['shop_id'])
        return Response(status=status.HTTP_201_CREATED)

    @swagger_auto_schema(
        responses={
            "200": AttentionLinkSerializer(),
        },
        operation_description="我的关注",
    )
    @action(methods=["get"], detail=False)
    def my_attention(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        queryset = queryset.filter(customer_id=request.user.userprofile.customer_id)
        person_list = CustomerListFetcher(queryset, request).data
        return Response(person_list, status=status.HTTP_200_OK)



