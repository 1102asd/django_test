from rest_framework import pagination
from django.utils.translation import gettext_lazy as _
from drf_yasg.inspectors import PaginatorInspector
from drf_yasg import openapi
from collections import OrderedDict


class PaginatorInspectorClass(PaginatorInspector):

    def get_paginated_response(self, paginator, response_schema):
        """
        :param BasePagination paginator: the paginator
        :param openapi.Schema response_schema: the response schema that must be paged.
        :rtype: openapi.Schema
        """

        return openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties=OrderedDict((
                ('count', openapi.Schema(type=openapi.TYPE_INTEGER)),
                ('next', openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties=OrderedDict((
                        ('page', openapi.Schema(type=openapi.TYPE_INTEGER)),
                        ('page_size', openapi.Schema(type=openapi.TYPE_INTEGER))
                    ))
                )),
                ('results', response_schema),
            )),
            required=['results']
        )

    def get_paginator_parameters(self, paginator):
        """
        Get the pagination parameters for a single paginator **instance**.

        Should return :data:`.NotHandled` if this inspector does not know how to handle the given `paginator`.

        :param BasePagination paginator: the paginator
        :rtype: list[openapi.Parameter]
        """

        return [
            openapi.Parameter('page', openapi.IN_QUERY, "页码数", False, None, openapi.TYPE_INTEGER),
            openapi.Parameter('page_size', openapi.IN_QUERY, "页大小", False, None, openapi.TYPE_INTEGER)
        ]


class BasePageNumberPagination(pagination.PageNumberPagination):
    page_size = 20
    page_size_query_param = 'page_size'
    max_page_size = 100
    page_query_description = _('支持不分页no_page')
    page_size_query_description = _('大数据量使用no_page会卡死')

    def paginate_queryset(self, queryset, request, view=None):
        if 'no_page' in request.query_params:
            return None
        return super(BasePageNumberPagination, self).paginate_queryset(queryset, request, view)


class BaseForcePageNumberPagination(pagination.PageNumberPagination):
    page_size = 20
    page_size_query_param = 'page_size'
    max_page_size = 100
