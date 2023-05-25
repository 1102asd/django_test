from rest_framework.viewsets import GenericViewSet

from django_test.utils.pagination import BasePageNumberPagination
# from bmims_common.operation_log import (
#     OperationLogMixin,
# )
from django_test.drf_expand_fields import ExpandFieldsModelViewSetMixin


class BaseGenericViewSet(ExpandFieldsModelViewSetMixin, GenericViewSet):
    pagination_class = BasePageNumberPagination
