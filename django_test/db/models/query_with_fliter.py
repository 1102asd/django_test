from ..registry import foreignkeys


def prefetch_related_objects_with_para(instances, lookups, para=None, order=None):
    """在原有的基础上对关联对象进行参数过滤，主要用于反向set
    para格式：Model为键，查询条件为值的字典嵌套，如查询职位有哪些在职的人
    prefetch_related_objects(Position.objects.all(), ['person_set'], {Person: {'status': '在职'}})
    order: {Person: ('status', '-update_time')}
    """
    _PrefetchManger(instances, lookups, para, order)


class _PrefetchManger(object):
    def __init__(self, instances, lookups, para=None, order=None):
        self.para = para or {}
        self.order = order or {}
        self._visit_instances(instances, lookups)

    def _visit_instances(self, instances, lookups):
        first_level, next_level = _split_lookup(lookups)
        if not first_level:
            return
        if not instances:
            return
        model = type(instances[0])
        fks = foreignkeys.get_foreign_keys(model)
        reverse_related_objs = foreignkeys.get_reverse_related_objects(model)
        for lookup in first_level:
            is_reverse = False
            if lookup.endswith('_set'):
                is_reverse = True
                reverse_relate_model_name = lookup[:-4]
                for from_model, rel_info in list(reverse_related_objs.items()):
                    if from_model.__name__.lower() == reverse_relate_model_name:
                        lookup_field = 'id'
                        relation_model = from_model
                        relation_field = rel_info['from_field']
                        break
                else:
                    continue
            else:
                lookup_field = lookup + '_id'
                relation_field = 'id'
                if lookup_field not in fks:
                    continue
                relation_model = fks[lookup_field]['to_model']
            lookup_ids = []
            for instance in instances:
                lookup_id = getattr(instance, lookup_field)
                if lookup_id is not None:
                    lookup_ids.append(lookup_id)
            qs = relation_model.objects.filter(**{'%s__in' % relation_field: lookup_ids}).order_by('-id')
            if relation_model in self.para:
                qs = qs.filter(**self.para[relation_model])
            if relation_model in self.order:
                qs = qs.order_by(*self.order[relation_model])
            relation_instances = list(qs)
            lookup_id_to_relation_instances = {}
            for relation_instance in relation_instances:
                lookup_id_to_relation_instances.setdefault(getattr(relation_instance, relation_field), []).append(relation_instance)
            # fill the cache
            for instance in instances:
                instance_lookup_result = lookup_id_to_relation_instances.get(getattr(instance, lookup_field), [])
                if not is_reverse:
                    instance_lookup_result = instance_lookup_result[0] if instance_lookup_result else None
                setattr(instance, lookup, instance_lookup_result)
            self._visit_instances(relation_instances, next_level.get(lookup, []))


def _split_lookup(lookups):
    first_level_lookup = []
    second_level_lookup = {}
    for lookup in lookups:
        pieces = lookup.split('__', 1)
        first = pieces[0]
        children = pieces[1:]
        if first:
            first_level_lookup.append(first)
            if children:
                second_level_lookup.setdefault(first, []).append(children[0])
    first_level_lookup = list(set(first_level_lookup))
    return first_level_lookup, second_level_lookup
