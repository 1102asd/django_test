# -*-coding:UTF-8-*-
"""
@Project : django_test
@File : use.py
@IDE : PyCharm
@Author : 何顺昌
@Date : 2023/5/2518:10
"""
from drf_yasg.utils import swagger_auto_schema
from rest_framework.response import Response

from django_user.views import BaseAPIView
from django_user.serializers import UserSerializer, UserPostSerializer


class UserAPIView(BaseAPIView):
    authentication_classes = ()
    permission_classes = ()

    @swagger_auto_schema(
        request_body=UserPostSerializer(),
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
        serializer.create(validated_data)
        return Response(data=serializer.validated_data)
