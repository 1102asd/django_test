from django.conf.urls import url, include
from rest_framework import routers

from django_user.views.auth import AuthTokenAPIView
from django_user.views.user import UserAPIView

router = routers.SimpleRouter()

urlpatterns = [
    url(r'^', include(router.urls)),
]
