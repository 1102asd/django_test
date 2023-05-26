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


class PointsPoorError(BaseError):
    code = 21
    message = '你的积分不足，不能邀请此人'


class NotExistError(BaseError):
    code = 22
    message = '专家不存在，无法邀请'


class UnFollowingError(BaseError):
    code = 24
    message = '未关注此问题'


class RepeatedFollowingError(BaseError):
    code = 25
    message = '已经关注此问题'


class QuestionNotFoundError(BaseError):
    code = 26
    message = '问题不存在'


class QuestionTypeRequiredError(BaseError):
    code = 27
    message = "问题类型为必选"


class TopicRequiredError(BaseError):
    code = 28
    message = "话题为必选"


class TopicNotFoundError(BaseError):
    code = 29
    message = "话题不存在"


class MaxChooseThreeError(BaseError):
    code = 31
    message = "最多选择三个"


class TagEmptyError(BaseError):
    code = 32
    message = "标签不能为空"


class RepeatSetBestAnswerError(BaseError):
    code = 33
    message = "已有最佳答案"


class AnswerNotFoundError(BaseError):
    code = 34
    message = "回答不存在或已被删除"


class UserNotAgreeError(BaseError):
    code = 35
    message = "用户还没有赞同过此回答"


class RepeatAgreeError(BaseError):
    code = 36
    message = "你已赞同过此答案"


class NotTelePhoneError(BaseError):
    code = 30
    message = '已经得到此人联系方式'


class RequestsError(BaseError):
    code = 40
    message = '请求失败'


class NotAreaError(BaseError):
    code = 50
    message = '获取地址信息失败'


class NotInquiryError(BaseError):
    code = 60
    message = '远程问诊错误'


class CrowdfundingError(BaseError):
    code = 70
    message = '众筹错误'


class AnnounceError(BaseError):
    code = 80
    message = '揭榜挂帅错误'


class UserNotExistError(BaseError):
    code = 90
    message = "用户不存在"


class InquirySettingNotExistError(BaseError):
    code = 91
    message = "该专家问诊设置错误"


class InquiryRecordNotExistError(BaseError):
    code = 92
    message = "未找到此条问诊记录"


class SensitiveError(BaseError):
    code = 120
    message = "敏感内容检测服务错误，请稍后重试"


class NoticeError(BaseError):
    code = 1000
    message = '通知消息失败，请稍后重试'


def diagnosis_error_handler(exc, context):
    if isinstance(exc, BaseError):
        response = JsonResponse(exc.get_response_data(), status=402)
    else:
        response = exception_handler(exc, context)
    return response
