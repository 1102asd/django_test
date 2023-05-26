# -*- coding: utf-8 -*-


from logging import getLogger

from django.http import JsonResponse
from django.contrib.auth import authenticate
from drf_yasg.utils import swagger_auto_schema
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.response import Response

from django_user.authentication import ExpiringTokenAuthentication
from .base import BaseAPIView
from ..serializers import AuthSerializer, UserSerializer
from ..models import ApiToken
from ..authentication import get_token_expires
from ..serializers.auth import AuthResponseSerializer

logger = getLogger('taps')


class AuthTokenAPIView(BaseAPIView):
    authentication_classes = ()
    permission_classes = ()

    def get_authenticate_header(self, request):
        return ExpiringTokenAuthentication().authenticate_header(request)

    @swagger_auto_schema(
        request_body=AuthSerializer(),
        responses={
            "200": AuthResponseSerializer(),
        },
        operation_description="获取用户 token, 使用 用户名和密码",
    )
    def post(self, request):
        """获取用户 token, 使用 用户名和密码。
        测试环境账号：test/123456
        """
        auth_serializer = AuthSerializer(data=request.data)
        if not auth_serializer.is_valid():
            return JsonResponse(auth_serializer.errors, status=400)
        # todo get info from session
        username = auth_serializer.validated_data['username']
        password = auth_serializer.validated_data.get('password')
        token_max_age = auth_serializer.validated_data['token_max_age']
        user = authenticate(username=username, password=password)
        if user is None or (not user.userprofile.is_enabled):
            raise AuthenticationFailed()
        token, _ = ApiToken.objects.get_or_create(user=user)
        if token.is_expired():
            token.delete()
            token, _ = ApiToken.objects.get_or_create(user=user)
        token.set_max_age(token_max_age)
        token.save()
        user_serialized = AuthResponseSerializer(user, partial=True)
        data = {
            'token': token.key,
            'expires': get_token_expires(token),
            'user': user_serialized.data,
            # 'tenant': request.tenant.name,
        }
        return Response(data=data)
