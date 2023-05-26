from rest_framework import serializers

from django_test.drf_expand_fields import ExpandFieldsModelSerializerMixin
from django_test.drf_expand_fields import ExpandFieldsWithSetModelSerializerMixin
from django_test.db.registry import foreignkeys
from .rest_remap_serializer import BaseRemapModelSerializer


class BaseModelSerializer(ExpandFieldsModelSerializerMixin, BaseRemapModelSerializer):
    class Meta:
        exclude = ['is_deleted']
        read_only_fields = ('create_time', 'update_time', 'create_user_id', 'update_user_id')
        depth = 0

    def get_fields(self):
        fields = super(BaseModelSerializer, self).get_fields()
        for field, foreign_info in list(foreignkeys.get_foreign_keys(self.Meta.model).items()):
            if field in fields:
                fields[field].validators.append(ForeignKeyExistsValidator(foreign_info['to_model'].objects))
        return fields


class BaseExtensionModelSerializer(ExpandFieldsWithSetModelSerializerMixin, BaseRemapModelSerializer):

    class Meta:
        exclude = ['is_deleted']
        read_only_fields = ('create_time', 'update_time', 'create_user_id', 'update_user_id')
        depth = 0

    def get_fields(self):
        fields = super().get_fields()
        for field, foreign_info in list(foreignkeys.get_foreign_keys(self.Meta.model).items()):
            if field in fields:
                fields[field].validators.append(ForeignKeyExistsValidator(foreign_info['to_model'].objects))
        return fields


class ForeignKeyExistsValidator(object):
    def __init__(self, queryset):
        self.queryset = queryset

    def __call__(self, value):
        if not self.queryset.filter(pk=value).exists():
            message = '无效主键 %s - 这个字段必须在关联对象中存在' % value
            raise serializers.ValidationError(message)
