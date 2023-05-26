# -*-coding:UTF-8-*-
"""
@Project : django_test
@File : use.py
@IDE : PyCharm
@Author : 何顺昌
@Date : 2023/5/2518:10
"""
from django.contrib.auth.hashers import make_password
from drf_yasg.utils import swagger_auto_schema
from rest_framework.response import Response
from django_user.models import BaseUser
from django_user.serializers import UserSerializer
from django_filters import rest_framework as filters

from django_test.rest.filters import BaseFilterSet
from django_user.views.base import BaseAPIView


class InquiryRecodingFilterSet(BaseFilterSet):
    recoding_status = filters.NumberFilter(
        help_text="1，进行中，0 已结束", method="get_query_recoding", required=True
    )

    class Meta:
        model = BaseUser
        fields = ["name"]


class UserAPIView(BaseAPIView):
    authentication_classes = ()
    permission_classes = ()

    @swagger_auto_schema(
        request_body=UserSerializer(),
        responses={
            "200": UserSerializer(),
        },
        operation_description="创建用户",
    )
    def post(self, request):
        data = request.data
        serializer = UserSerializer(data=data, partial=True)
        serializer.is_valid(raise_exception=True)
        validated_data = serializer.validated_data
        validated_data['password'] = make_password(validated_data['password'])
        serializer.create(validated_data)
        return Response(data=serializer.validated_data)
