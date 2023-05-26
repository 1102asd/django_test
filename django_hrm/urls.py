from django.conf.urls import url, include
from rest_framework import routers

from django_hrm.views.customer import CustomerCreateAPIView

router = routers.SimpleRouter()

urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^create-customer/$', CustomerCreateAPIView.as_view(), name='create-customer'),
]
