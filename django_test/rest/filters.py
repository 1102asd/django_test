from django_filters import rest_framework as filters
import datetime
import django_filters
from django import forms
from django.utils.encoding import force_str
from django_filters.filters import (
    BaseInFilter,
    NumberFilter,
)


class NumberInFilter(BaseInFilter, NumberFilter):
    pass


class BaseFilterSet(filters.FilterSet):
    pass


class MaxDate(forms.DateField):
    """
    用日期查询DateTime格式日期, 将结束日期Date转为最大值的DateTime格式
    """
    def to_python(self, value):
        """
        Validates that the input can be converted to a date. Returns a Python
        datetime.date object.
        """
        if value in self.empty_values:
            return None
        if isinstance(value, datetime.datetime):
            return datetime.datetime.combine(value.date(), datetime.time.max)
        if isinstance(value, datetime.date):
            return datetime.datetime.combine(value, datetime.time.max)
        return super(MaxDate, self).to_python(value)

    def strptime(self, value, format):
        date = datetime.datetime.strptime(force_str(value), format).date()
        return datetime.datetime.combine(date, datetime.time.max)


class MaxDateFilter(django_filters.Filter):
    field_class = MaxDate