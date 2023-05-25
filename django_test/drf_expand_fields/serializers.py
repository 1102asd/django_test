# -*- coding: utf-8 -*-
import importlib

from django_test.db.registry import foreignkeys


class ExpandFieldsModelSerializerMixin(object):
    """A ModelSerializer mixin that uses expand to control whether fields
    should do nested serialization.
    """
    def __init__(self, *args, **kwargs):
        self.expanded_fields = []
        super(ExpandFieldsModelSerializerMixin, self).__init__(*args, **kwargs)
        expand = self.context.get('expand', [])
        expand_fields, next_level_expand = _split_expand(expand)
        for field in self._get_expandable_fields(expand_fields):
            self.fields[field] = self._build_expanded_field_serializer(field, next_level_expand.get(field))
            self.expanded_fields.append(field)

    def _get_expandable_fields(self, expand_fields):
        if not expand_fields:
            return []
        expandable = []
        for field in expand_fields:
            if not self._get_to_model(field):
                continue
            expandable.append(field)
        return expandable

    def _build_expanded_field_serializer(self, field, expand):
        to_model = self._get_to_model(field)
        serializer_class_name = '{}.serializers.{}Serializer'.format(to_model._meta.app_label, to_model.__name__)
        serializer_class = self._import_serializer_class(serializer_class_name)
        return serializer_class(context={'expand': expand})

    def _get_to_model(self, field):
        foreign_info = foreignkeys.get_foreign_keys(self.Meta.model).get(_add_field_id(field))
        return foreign_info['to_model'] if foreign_info else None

    def _import_serializer_class(self, serializer_class_name):
        mod, cls = serializer_class_name.rsplit('.', 1)
        module = importlib.import_module(mod)
        return getattr(module, cls)

    def to_representation(self, instance):
        # 在这里把需要展开的对象获取到
        for field in self.expanded_fields:
            if not hasattr(instance, field):
                setattr(instance, field, self._get_to_instance(instance, field))
        ret = super(ExpandFieldsModelSerializerMixin, self).to_representation(instance)
        return ret

    def _get_to_instance(self, instance, field):
        to_model = self._get_to_model(field)
        return to_model.objects.filter(pk=getattr(instance, _add_field_id(field))).first()


def _add_field_id(field):
    # 外键 post，转为 post_id
    return field + '_id'


def _split_expand(expand):
    """Convert ['a', 'a.b', 'a.b.c', 'd'] to:

    first_level: ['a', 'd']
    next_level: {'a': ['b', 'b.c']}
    """
    first_level_fields = []
    next_level_fields = {}

    if not expand:
        return first_level_fields, next_level_fields
    for field in expand:
        if '.' in field:
            first_level, next_level = field.split('.', 1)
            first_level_fields.append(first_level)
            next_level_fields.setdefault(first_level, []).append(next_level)
        else:
            first_level_fields.append(field)
    first_level_fields = list(set(first_level_fields))
    return first_level_fields, next_level_fields
