from django.db import models
from rest_framework.fields import DecimalField
from rest_framework import serializers
from rest_framework.serializers import raise_errors_on_nested_writes
from rest_framework.utils import model_meta

from django_test.rest.fields import NormalizedDecimalField


class BaseRemapModelSerializer(serializers.ModelSerializer):
    serializer_field_mapping = {
        **serializers.ModelSerializer.serializer_field_mapping,
        **{models.DecimalField: NormalizedDecimalField}
    }

    def update(self, instance, validated_data):
        raise_errors_on_nested_writes('update', self, validated_data)
        info = model_meta.get_field_info(instance)

        m2m_fields = []
        update_fields = []
        for attr, value in validated_data.items():
            if attr in info.relations and info.relations[attr].to_many:
                m2m_fields.append((attr, value))
            else:
                setattr(instance, attr, value)
                update_fields.append(attr)
        # NOTE: 同时对同一个资源请求的patch方法，后一个可能会覆盖前一个的修改
        # 对于patch方法只更新对应的修改字段
        # 不指定update_time，save不会更新auto_now的值
        if hasattr(instance, 'update_time'):
            update_fields.append('update_time')
        if hasattr(instance, 'update_user_id'):
            update_fields.append('update_user_id')
        instance.save(update_fields=update_fields)
        for attr, value in m2m_fields:
            field = getattr(instance, attr)
            field.set(value)

        return instance
