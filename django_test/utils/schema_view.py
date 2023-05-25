from drf_yasg.generators import EndpointEnumerator
from rest_framework import permissions
from rest_framework import serializers
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from drf_yasg.app_settings import swagger_settings
from drf_yasg.inspectors import ChoiceFieldInspector, SwaggerAutoSchema
from drf_yasg.generators import OpenAPISchemaGenerator


class ChoiceFieldWithDisplayNameInspector(ChoiceFieldInspector):
    def field_to_swagger_object(self, field, swagger_object_type, use_references, **kwargs):
        result = super().field_to_swagger_object(field, swagger_object_type, use_references, **kwargs)
        if isinstance(field, serializers.ChoiceField):
            if hasattr(result, 'description'):
                result.description += ', %s' % dict(field.choices)
            else:
                result.description = str(dict(field.choices))

        return result


field_inspectors = []
for inspector in swagger_settings.DEFAULT_FIELD_INSPECTORS:
    if inspector == ChoiceFieldInspector:
        field_inspectors.append(ChoiceFieldWithDisplayNameInspector)
    else:
        field_inspectors.append(inspector)


class BmimsSwaggerAutoSchema(SwaggerAutoSchema):
    field_inspectors = field_inspectors


class CustomOpenAPISchemaGenerator(OpenAPISchemaGenerator):

    def get_schema(self, *args, **kwargs):
        schema = super().get_schema(*args, **kwargs)
        for path_key, path in schema.paths.items():
            for op in path.operations:
                if not hasattr(op[1], 'summary'):
                    # 给api添加标题
                    op[1].summary = op[1].description.strip().split('\n')[0]
        return schema


schema_view = get_schema_view(
    openapi.Info(title="diagnosis API", default_version='v1',),
    public=True,
    permission_classes=(permissions.AllowAny,),
    generator_class=CustomOpenAPISchemaGenerator,
)
