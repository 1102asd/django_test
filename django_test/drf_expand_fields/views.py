# -*- coding: utf-8 -*-
from django_test.db.registry import foreignkeys
from django_test.db.models import prefetch_related_objects


class ExpandFieldsModelViewSetMixin(object):
    """A ModelViewSet mixin that uses expand to control whether fields
    should do nested serialization.

    例如，默认请求 /comments/1/ 获取到 {"post_id": 123}，
    这时候你可以请求 /comments/1/?expand=post，然后获取到
     {"post_id": 123, "post": {"id": 123, "content": "my post"}}。
    你可以递归进行扩展，针对嵌套的字段使用 "." 就可以。例如，
    请求 /comments/1/?expand=post.user，然后可以同时扩展 post
    和 post 内的 user。
    一次多个嵌套可以用 "," 分隔，比如 /comments/1/?expand=post,user 。

    如果需要 ViewSet 级别的默认 expand，可以进行如下设置 ::

        class BaseModelViewSet(ExpandFieldsModelViewSetMixin, viewsets.ModelViewSet):
            expand_fields = ['post.user', 'user']
    """
    # View level expand context
    expand_fields = []

    def get_serializer_context(self):
        context = super(ExpandFieldsModelViewSetMixin, self).get_serializer_context()
        expand = self._get_expand_fields()
        if expand:
            context['expand'] = expand
        return context

    def get_serializer(self, *args, **kwargs):
        expand = self._get_expand_fields()
        if expand and self.request.method.lower() == 'get' and args:
            try:
                iter(args[0])
                lookups = [e.replace('.', '__') for e in expand]
                prefetch_related_objects(args[0], *lookups)
            except TypeError:
                pass
        return super(ExpandFieldsModelViewSetMixin, self).get_serializer(*args, **kwargs)

    def _parse_request_expand(self):
        value = self.request.query_params.get('expand')
        return value.split(',') if value else []

    def _get_extra_models(self):
        """Extra models that is returned by this models viewset other
        than the queryset.models"""
        extra_models = []
        expand_fields = self._get_expand_fields()
        for field in expand_fields:
            field_list = field.split('.')
            if hasattr(self, 'get_queryset'):
                model = self.get_queryset().model
            else:
                model = self.queryset.model
            for f in field_list:
                foreign_info = foreignkeys.get_foreign_keys(model).get(f + '_id')
                if foreign_info:
                    extra_models.append(foreign_info['to_model'])
                else:
                    break
                model = f
        return set(extra_models)

    def _get_expand_fields(self):
        expand_fields = []
        if self.request.method == "GET":
            if self.expand_fields:
                expand_fields = self.expand_fields
            else:
                expand_fields = self._parse_request_expand()
        return expand_fields
