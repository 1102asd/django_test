# -*- coding: utf-8 -*-
from django.apps import apps


class ForeignKeyConstraintRegistry(object):
    """A registry that stores all foreign key constrants.
    It also provides reverse-relations.

    我们采用自己应用逻辑控制的 Foreign Key，定义一个外键约束的方式为：

    class Comment(models.Model):
        class ForeignKeyConstraint:
            fields = {
                "post_id": {"to_model": "blog.Post"},
                # if you do not provide on_delete, it defaults to PROTECT
                "author_id": {"to_model": "blog.Post", "on_delete": DO_NOTHING},
            }
    """
    def __init__(self):
        self._constraints = None

    @property
    def constraints(self):
        if self._constraints is None:
            self._build_constraints()
        return self._constraints

    def _build_constraints(self):
        if not apps.ready:
            raise RuntimeError("App registry isn't ready yet.")
        from .models.deletion import PROTECT
        relations = {}
        reverse_relations = {}
        for app_conf in apps.get_app_configs():
            for model in app_conf.get_models():
                if not hasattr(model, 'ForeignKeyConstraint'):
                    continue
                foreign_keys = {}
                for field, fk_info in list(model.ForeignKeyConstraint.fields.items()):
                    to_model = apps.get_model(fk_info['to_model'])
                    foreign_keys[field] = {'to_model': to_model}
                    reverse_relations.setdefault(to_model, {})[model] = \
                        {'from_field': field, 'on_delete': fk_info.get('on_delete', PROTECT)}
                if foreign_keys:
                    relations[model] = foreign_keys
        self._constraints = relations, reverse_relations

    def get_foreign_keys(self, model):
        """Foreign keys that are defined in this models

        Comment -> {"post_id": {"to_model": Post}}
        """
        relations, _ = self.constraints
        return relations.get(model, {})

    def get_reverse_related_objects(self, model):
        """Foreign Keys pointing to this models from other models.

        Post -> {Comment: {"from_field": "post_id"}}
        """
        _, reverse_relations = self.constraints
        return reverse_relations.get(model, {})


foreignkeys = ForeignKeyConstraintRegistry()
