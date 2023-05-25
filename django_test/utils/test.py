from django.contrib.auth.models import User
from django.test import TestCase
from rest_framework.test import APITestCase

from django_user.models import ApiToken


class BaseTestCase(TestCase):
    @classmethod
    def setUpClass(cls):
        super(TestCase, cls).setUpClass()

    def setUp(self) -> None:
        super(BaseTestCase, self).setUp()


class BaseAPITestCase(APITestCase):
    def __init__(self, methodName="runTest"):
        super(BaseAPITestCase, self).__init__(methodName)
        self.user = None
        self.token = None

    @classmethod
    def setUpClass(cls):
        super(BaseAPITestCase, cls).setUpClass()

    def init_user(self, user):
        token, _ = ApiToken.objects.get_or_create(user=user)
        token.set_max_age()
        self.token = token
        person, _ = User.objects.get_or_create(name="test_person")
        user.userprofile.person_id = 1
        user.userprofile.score_value = 500
        user.userprofile.save()

    def set_current_user(self):
        """
        当需要测试某种功能的权限时，可通过本方法设置当前用户，使用该用户访问API，返回None时为匿名用户
        """
        self.user, _ = User.objects.get_or_create(
            id=10000,
            username="test_user",
        )

    def init(self):
        self.set_current_user()
        if self.user:
            self.init_user(self.user)

    def setUp(self):
        self.init()
        if self.token:
            self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.token.key}")
