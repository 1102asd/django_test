# -*- coding: utf-8 -*-
import importlib

from django_test.db.registry import foreignkeys
from .serializers import _split_expand, _add_field_id
from django_test.utils.rest_remap_serializer import BaseRemapModelSerializer


class ExpandFieldsWithSetModelSerializerMixin(object):
    """在ExpandFieldsModelSerializerMixin基础上支持反向set操作:
    用户发微博:
    class User:
        pass
    class Blog:
        # 简写只是表达关系
        user = User
    获取用户发的所有微博
    GET /users/1/?expand=blog_set
    {
        "user_id": 1,
        "blog_set": [
            {"id": 1, "user_id": 1},
            {"id": 2, "user_id": 1},
        ]
    }
    # note: 不支持一个表的两个外键字段都指向一个表的反向set操作，如：
    # 使用Django的原生ForeignKey会直接报错，此类关系应该使用ManyToMany关系
    # 本项目可以使用Mapping关联
    class Blog:
        user1 = User
        user2 = User
    执行GET /users/1/?expand=blog_set只能获取之中一个user的blog set
    """
    def __init__(self, *args, **kwargs):
        super(ExpandFieldsWithSetModelSerializerMixin, self).__init__(*args, **kwargs)
        expand = self.context.get('expand', [])
        expand_fields, next_level_expand = _split_expand(expand)
        self.expanded_fields = self._get_expandable_fields(expand_fields)

        for field, model_info in self.expanded_fields.items():
            self.fields[field] = self._build_expanded_field_serializer(model_info, next_level_expand.get(field))

    def _get_expandable_fields(self, expand_fields):
        if not expand_fields:
            return {}
        expandable = {}
        for field in expand_fields:
            if to_model := self._get_to_model(field):   # noqa
                expandable[field] = ('to_model', to_model)
            elif from_info := self._get_from_model(field): # noqa
                from_model, from_field = from_info
                expandable[field] = ('from_model', from_model, from_field)
            else:
                continue
        return expandable

    def _build_expanded_field_serializer(self, model_info, expand):
        model = model_info[1]
        # serializer_class_name = '{}.serializers.{}Serializer'.format(models._meta.app_label, models.__name__)
        # serializer_class = self._import_serializer_class(serializer_class_name)
        serializer_class = get_expand_serializer_class(model)
        if model_info[0] == 'to_model':
            return serializer_class(context={'expand': expand})
        else:
            return serializer_class(context={'expand': expand}, many=True)

    def _get_to_model(self, field):
        foreign_info = foreignkeys.get_foreign_keys(self.Meta.model).get(_add_field_id(field))
        return foreign_info['to_model'] if foreign_info else None

    def _get_from_model(self, field):
        if not field.endswith('_set'):
            return None
        model = self.Meta.model
        reverse_relate_model_name = field[:-4]
        reverse_related_objs = foreignkeys.get_reverse_related_objects(model)
        for from_model, from_field in list(reverse_related_objs.items()):
            if from_model.__name__.lower() == reverse_relate_model_name:
                return from_model, from_field['from_field']
        return None

    def _import_serializer_class(self, serializer_class_name):
        mod, cls = serializer_class_name.rsplit('.', 1)
        module = importlib.import_module(mod)
        return getattr(module, cls)

    def to_representation(self, instance):
        # 在这里把需要展开的对象获取到
        for field, model_info in self.expanded_fields.items():
            if not hasattr(instance, field):
                if model_info[0] == 'to_model':
                    setattr(instance, field, self._get_to_instance(instance, field, model_info[1]))
                else:
                    setattr(instance, field, self._get_from_instance(instance, model_info[2], model_info[1]))

        ret = super(ExpandFieldsWithSetModelSerializerMixin, self).to_representation(instance)
        return ret

    def _get_to_instance(self, instance, field, to_model):
        return to_model.objects.filter(pk=getattr(instance, _add_field_id(field))).first()

    def _get_from_instance(self, instance, from_field, from_model):
        return from_model.objects.filter(**{from_field: instance.id})


def get_expand_serializer_class(model):
    # 动态生成Model对应的ModelSerializer
    sub_class = type("Meta", (), {"models": model, "exclude": [
        'is_deleted', 'create_user_id', 'update_user_id', 'source_id']})
    return type(f"Expand{model.__name__}Serializer",
                (ExpandFieldsWithSetModelSerializerMixin, BaseRemapModelSerializer), {"Meta": sub_class})
