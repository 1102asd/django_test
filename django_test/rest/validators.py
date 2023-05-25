from rest_framework import serializers


class ForeignKeyExistsValidator:
    def __init__(self, queryset, label=None):
        if label is None:
            label = queryset.model.__name__
        self.queryset = queryset
        self.label = label

    def __call__(self, value):
        if not self.queryset.filter(pk=value).exists():
            message = '不存在的 <%s: %s>' % (self.label, value)
            raise serializers.ValidationError(message)
