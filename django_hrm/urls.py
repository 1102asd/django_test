from django.conf.urls import url, include
from rest_framework import routers

from django_hrm.views import ShopViewSet
from django_hrm.views.attentionlink import AttentionLinkViewSet
from django_hrm.views.business import BusinessCreateAPIView, BusinessUpdateAPIView
from django_hrm.views.customer import CustomerCreateAPIView, CustomerUpdateAPIView


router = routers.SimpleRouter()
router.register(r'customer-attention', AttentionLinkViewSet, basename='customer-attention')
router.register(r'shop', ShopViewSet, basename='shop')

urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^create-customer/$', CustomerCreateAPIView.as_view(), name='create-customer'),
    url(r'^update-customer/$', CustomerUpdateAPIView.as_view(), name='update-customer'),
    url(r'^create-business/$', BusinessCreateAPIView.as_view(), name='create-business'),
    url(r'^update-business/$', BusinessUpdateAPIView.as_view(), name='update-business'),
]
