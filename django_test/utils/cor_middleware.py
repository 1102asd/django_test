from django.utils.deprecation import MiddlewareMixin
from corsheaders.middleware import CorsMiddleware


class VueCorMiddleware(CorsMiddleware):

    def process_response(self, request, response):
        response = super(VueCorMiddleware, self).process_response(request, response)
        # response['Access-Control-Allow-Origin'] = request.META.get("HTTP_ORIGIN", "*")
        # response['Access-Control-Allow-Credentials'] = "true"
        return response
