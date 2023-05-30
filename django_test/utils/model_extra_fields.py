import abc
from functools import partial
from django_test.db.models import prefetch_related_objects


class InitialDataBase(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def get_data(self):
        pass


class ModelExtraFieldsBase(object):
    """
    可配置扩展字段基类
    """
    def __init__(self, mappings, obj_list, ser_class=None):
        """
        :param mappings:
        {
            'display_field_name': [
                relation,
                field name/get field data callable,
                {
                    "convert": result convert callable,
                    "default": field default value, default None,
                    "initial": initial data class --> see example: ReportData
                }
            ],
            ---- examples ----
            'work_order_codes': ['scannerplanmerge_set__work_job__parent_order', self._get_merged_order_codes],
            'rgb': ['work_order__color', 'rgb', {'default': 0, 'convert': convert_func}],

            if you define:
            class ReportData:
                def __init__(self, work_order_ids):
                    ....

                # you must implement this method
                def get_data(self):
                    result = {
                        'abc': 1
                    }
                    return result

            in mappings you have:
            'report_data': ['some_relations', self._get_func, {'initial': ReportData}]

            then after initializing the child class of ModelExtraFieldsBase, you can use:
            b = self.initials['abc'] + 1
            now the value of variable b is 2
        }
        :param obj_list: objects list that need extra fields of its relational objects
        """
        self.expand_mappings = mappings
        self.objs = obj_list
        self.serializer_class = ser_class
        self.initials = {}
        self.global_initial()

    def global_initial(self):
        initial_classes = set()
        initials = []
        for name, config in self.expand_mappings.items():
            if isinstance(config, list) and len(config) > 2:
                c = config[2].get('initial')
                if c is None:
                    continue
                if isinstance(c, partial):
                    _class = c.func
                else:
                    _class = c
                if _class not in initial_classes:
                    initial_classes.add(_class)
                    initials.append(c)

        fields = set()
        for c in initials:
            if isinstance(c, partial):
                data = c().get_data()
            else:
                data = c(self.objs).get_data()
            for field_name, value in data.items():
                if field_name in fields:
                    raise ValueError('field name {} conflict, please rename initial data class {} '
                                     'method get_data return values field name'.format(field_name, c.__name__))
            self.initials.update(data)

    @property
    def data(self):
        objs = self.get_flatten_prefetch_related_objects()
        result = []
        for obj in objs:
            data = self.get_instance_fields(obj)
            result.append(data)
        return result

    def get_flatten_prefetch_related_objects(self, fields=None):
        if fields is None:
            fields = self.default_fields()
        if not fields or not isinstance(fields, list):
            fields = self.default_fields()
        args = self._get_query_args(fields)
        fields = self._get_relation_field_names(args)
        prefetch_related_objects(self.objs, *args)
        flatten_func = partial(self._flatten_instance, fields=fields)
        return list(map(flatten_func, self.objs))

    def _get_query_args(self, display_fields):
        args = set()
        expand_fields = []
        for field_name in display_fields:
            if not isinstance(self.expand_mappings[field_name], list):
                continue
            relations = self.expand_mappings[field_name][0]
            if relations == 'self':
                continue
            elif isinstance(relations, list):
                expand_fields.extend(relations)
            elif isinstance(relations, str):
                expand_fields.append(relations)

        expand_fields.sort(key=lambda e: -len(e))
        for arg in expand_fields:
            if arg in args or any([k.startswith('{}__'.format(arg)) for k in args]):
                continue
            else:
                args.add(arg)
        return args

    def _get_relation_field_names(self, relations):
        result = set()
        for e in relations:
            result.add(e)
            count = e.count('__')
            for i in range(count):
                elem, *_ = e.rsplit('__', i + 1)
                result.add(elem)
        return result

    def _flatten_instance(self, instance, fields):
        for f in fields:
            name = f
            relations = f.split('__')
            obj = instance
            for r in relations:
                if hasattr(obj, r):
                    obj = getattr(obj, r)
                else:
                    obj = None
                    break
            setattr(instance, name, obj)
        return instance

    def get_instance_fields(self, obj, fields=None):
        if fields is None:
            fields = self.default_fields()
        if self.serializer_class:
            result = self.serializer_class(obj).data
        else:
            result = {}
        for f in fields:
            if f not in self.expand_mappings:
                continue
            if not isinstance(self.expand_mappings[f], list):
                v = self.expand_mappings[f]
                if callable(v):
                    result[f] = v(obj)
                    continue
                result[f] = v
                continue
            name, get_name, *kwargs = self.expand_mappings[f]
            if isinstance(get_name, str):
                if name == 'self':
                    result[f] = getattr(obj, get_name)
                else:
                    relate_obj = getattr(obj, name)
                    result[f] = getattr(relate_obj, get_name) if relate_obj else None
            elif callable(get_name):
                result[f] = get_name(obj)
            default_value = kwargs[0].get('default', None) if len(kwargs) else None
            if result[f] is None:
                result[f] = default_value
            convert = kwargs[0].get('convert') if len(kwargs) else None
            if result[f] is not None and callable(convert):
                result[f] = convert(result[f])
        return result

    def default_fields(self):
        return list(self.expand_mappings.keys())
