# -*-coding:UTF-8-*-
"""
@Project : django_test
@File : authentication.py
@IDE : PyCharm
@Author : 何顺昌
@Date : 2023/5/2518:13
"""
# -*- coding: utf-8 -*-
from datetime import timedelta

import threading
from rest_framework.authentication import TokenAuthentication
from rest_framework.exceptions import AuthenticationFailed
from django.utils.translation import ugettext_lazy as _

_auth_ctx = threading.local()


class ExpiringTokenAuthentication(TokenAuthentication):
    def get_model(self):
        from django_user.models import ApiToken
        return ApiToken

    def _get_auth_token(self, key):
        user, token = super(ExpiringTokenAuthentication, self).authenticate_credentials(key)
        return user, token

    def authenticate_credentials(self, key):
        user, token = self._get_auth_token(key)
        if not user.userprofile.is_enabled:
            raise AuthenticationFailed(_('User disabled.'))
        # if token.is_expired():
        #     raise AuthenticationFailed(_('Invalid token.'))
        setattr(_auth_ctx, 'user', user)
        setattr(user, 'type', user.userprofile.type)
        setattr(user, 'name', user.userprofile.name)
        return user, token


def get_token_expires(token):
    expires_time = token.expires.isoformat()
    if expires_time.endswith('+00:00'):
        expires_time = expires_time[:-6] + 'Z'
    return expires_time
