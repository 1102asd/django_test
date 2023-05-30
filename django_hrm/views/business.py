# -*-coding:UTF-8-*-
"""
@Project : django_test
@File : business.py
@IDE : PyCharm
@Author : 何顺昌
@Date : 2023/5/2615:33
"""
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.response import Response

from django_hrm.models import Customer, Business
from django_hrm.serializers import CreateCustomerSerializer
from django_hrm.serializers.business import UpdateBusinessSerializer
from django_user.authentication import get_token_expires
from django_user.models import UserProfile
from django_user.serializers import UserSerializer
from django_user.serializers.auth import AuthResponseSerializer
from django_user.views.base import BaseAPIView


class BusinessCreateAPIView(BaseAPIView):
    permission_classes = ()
    authentication_classes = ()

    @swagger_auto_schema(
        request_body=CreateCustomerSerializer(),
        responses={
            "200": AuthResponseSerializer(),
        },
        operation_description="商家登录页 不存在直接创建，存在返回token",
    )
    def post(self, request):
        auth_serializer = CreateCustomerSerializer(data=request.data)
        auth_serializer.is_valid(raise_exception=True)
        data = auth_serializer.validated_data
        token_obj, user = Business.login(data['username'], data['password'])
        token_obj.set_max_age(data['token_max_age'])
        token_obj.save()
        user_serialized = UserSerializer(user, partial=True)

        data = {
            'token': token_obj.key,
            'expires': get_token_expires(token_obj),
            'user': user_serialized.data
        }
        return Response(data, status=200)


class BusinessUpdateAPIView(BaseAPIView):

    @swagger_auto_schema(
        request_body=UpdateBusinessSerializer(),
        responses={
            "200": UpdateBusinessSerializer(),
        },
        operation_description="商家修改个人信息",
    )
    def put(self, request, *args, **kwargs):
        person_serializer = UpdateBusinessSerializer(data=request.data)
        person_serializer.is_valid(raise_exception=True)
        validated_data = person_serializer.validated_data
        Business.objects.filter(id=request.user.business_id).update(**validated_data)
        UserProfile.objects.filter(id=request.user.userprofile.id).update(name=validated_data['name'])
        return Response(person_serializer.data, status=status.HTTP_200_OK)
