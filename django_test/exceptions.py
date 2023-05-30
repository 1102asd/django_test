from rest_framework.views import exception_handler
from django.http import JsonResponse


class BaseError(Exception):
    """不要直接使用这个类，请继承然后抛出异常。

    code 小于 20 的为保留编码。
    继承类 code 编码从 20 开始，递增。
    理论上，前端需要判定某种特定错误的，必须继承一个新类开一个新 Code，从而让前端判断。
    请求参数异常的，请自行处理用 400 返回异常，不要使用这个基类。
    """
    code = 1
    message = 'API 应用错误'

    def __init__(self, message=None):
        if message is not None:
            self.message = message

    def __str__(self):
        return self.message

    def get_response_data(self):
        return {"errors": [{"code": self.code, "message": self.message}]}

    def __repr__(self):
        return '<%s>' % self.__class__.__name__


class ModelProtectedError(BaseError):
    code = 20
    message = '此资源被其他资源依赖，无法删除'


class UserPasswordError(BaseError):
    code = 30
    message = '用户名已存在，密码错误'


def diagnosis_error_handler(exc, context):
    if isinstance(exc, BaseError):
        response = JsonResponse(exc.get_response_data(), status=402)
    else:
        response = exception_handler(exc, context)
    return response
