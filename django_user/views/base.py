# -*- coding: utf-8 -*-
from rest_framework import viewsets
from rest_framework.views import APIView

from django_test.utils.pagination import BasePageNumberPagination


class BasePaginationMixin(object):

    @property
    def paginator(self):
        """
        The paginator instance associated with the view, or `None`.
        """
        if not hasattr(self, '_paginator'):
            if self.pagination_class is None:
                self._paginator = None
            else:
                self._paginator = self.pagination_class()
        return self._paginator

    def paginate_queryset(self, queryset, request):
        """
        Return a single page of results, or `None` if pagination
        is disabled.
        """
        if self.paginator is None:
            return None
        return self.paginator.paginate_queryset(queryset, self.request, view=self)

    def get_paginated_response(self, data):
        """
        Return a paginated style `Response` object for the given
        output data.
        """
        assert self.paginator is not None
        return self.paginator.get_paginated_response(data)


class BaseModelViewSet(viewsets.ModelViewSet):
    pagination_class = BasePageNumberPagination

    def perform_destroy(self, instance):
        instance.on_delete()
        super(BaseModelViewSet, self).perform_destroy(instance)


class BaseReadOnlyModelViewSet(viewsets.ReadOnlyModelViewSet):
    pagination_class = BasePageNumberPagination


class BaseAPIView(APIView):
    pagination_class = BasePageNumberPagination
