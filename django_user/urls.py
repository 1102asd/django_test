from django.conf.urls import url, include
from rest_framework import routers

from django_user.views.auth import AuthTokenAPIView
from django_user.views.user import UserAPIView

router = routers.SimpleRouter()

urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^auth/token/$', AuthTokenAPIView.as_view(), name='auth-token'),
    url(r'^create-user/$', UserAPIView.as_view(), name='create-user'),
]
