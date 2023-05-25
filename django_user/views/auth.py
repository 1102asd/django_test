# -*- coding: utf-8 -*-


from logging import getLogger

from django.http import JsonResponse
from django.contrib.auth import authenticate
from rest_framework.exceptions import AuthenticationFailed

from django_user.authentication import ExpiringTokenAuthentication
from .base import BaseAPIView
from ..serializers import AuthSerializer, UserSerializer
from ..models import ApiToken
from ..authentication import get_token_expires


logger = getLogger('taps')


class AuthTokenAPIView(BaseAPIView):
    authentication_classes = ()
    permission_classes = ()

    def get_authenticate_header(self, request):
        return ExpiringTokenAuthentication().authenticate_header(request)

    def post(self, request):
        """获取用户 token, 使用 用户名和密码。

        request data:

        {
            "type": 0,  # 0 个人侧， 1 企业侧, 2 政府侧
            "token_max_age": 30,  # 单位为天
            "username": "person_1", # 用户名, 当用户名和对应type不一致的时候，以username 为主
        }

        response data:

        {
            "token": "abcddemo",
            "expires": "2013-01-29T12:34:56.000000Z"     # 过期时间，ISO 8601 格式
        }

        然后使用如下 HTTP Header:

        ```
         Authorization: Token 9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b
        ```

        测试环境账号：admin/123456
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
        user_serialized = UserSerializer(user)
        data = {
            'token': token.key,
            'expires': get_token_expires(token),
            'user': user_serialized.data,
            # 'tenant': request.tenant.name,
        }
        return JsonResponse(data)
