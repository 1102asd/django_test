from django_test.exceptions import ModelProtectedError
from ..registry import foreignkeys


PROTECT = 1
CASCADE = 2
SET_NULL = 3
DO_NOTHING = 4


class ModelOnDeleteMixin(object):
    def on_delete(self):
        on_delete_handler([self])


def on_delete_handler(objs):
    if not objs:
        return
    for model, rel_info in list(foreignkeys.get_reverse_related_objects(type(objs[0])).items()):
        on_delete_behavior = rel_info['on_delete']
        filter_kwargs = {
            '%s__in' % rel_info['from_field']: [obj.pk for obj in objs],
        }
        sub_objs = model.objects.filter(**filter_kwargs)
        if on_delete_behavior == PROTECT:
            if sub_objs.exists():
                msg = "无法删除，被别的资源依赖"
                raise ModelProtectedError(msg)
        elif on_delete_behavior == CASCADE:
            sub_objs.delete()
        elif on_delete_behavior == SET_NULL:
            sub_objs.update(**{rel_info['from_field']: None})
        elif on_delete_behavior == DO_NOTHING:
            pass
        else:
            raise RuntimeError('Unsupported on delete behavior.')
