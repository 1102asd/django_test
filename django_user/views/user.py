# -*-coding:UTF-8-*-
"""
@Project : django_test
@File : use.py
@IDE : PyCharm
@Author : 何顺昌
@Date : 2023/5/2518:10
"""
from django.contrib.auth.models import User
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.response import Response

from django_user.serializers.user import UserPasswordSerializer
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


class UserUpdatePasswordAPIView(BaseAPIView):
    @swagger_auto_schema(
        request_body=UserPasswordSerializer(),
        responses={
            "200": UserSerializer(),
        },
        operation_description="修改密码",
    )
    def put(self, request):
        data = request.data
        serializer = UserSerializer(data=data, partial=True)
        serializer.is_valid(raise_exception=True)
        validated_data = serializer.validated_data
        user_obj = User.objects.get(id=request.user.id)
        user_obj.set_password(validated_data['password'])
        user_obj.save()
        return Response(status=status.HTTP_200_OK)
