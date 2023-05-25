from kazoo.client import KazooClient

from .base import *


class ZookeeperSettings:
    def __init__(self):
        self.hosts = os.environ["ZK_HOSTS"]
        self.root_path = os.environ["ZK_ROOT_PARH"]
        self.zk = KazooClient(hosts=self.hosts, read_only=True)

    def __enter__(self):
        self.zk.start()
        return self

    def __getattr__(self, name):
        path = self.root_path + name
        if not self.zk.exists(path):
            raise AttributeError("Setting key doesn't exist: '%s'" % name)
        value = self.zk.get(path)[0].decode("utf-8")
        if value == "True":
            value = True
        elif value == "False":
            value = False
        return value

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.zk.stop()


with ZookeeperSettings() as zk_settings:
    DEBUG = zk_settings.DEBUG
    DATABASES_TIDB_HOST = zk_settings.DATABASES_TIDB_HOST
    DATABASES_TIDB_PASSWORD = zk_settings.DATABASES_TIDB_PASSWORD
    DATABASES_TIDB_PORT = zk_settings.DATABASES_TIDB_PORT
    DATABASES_TIDB_USER = zk_settings.DATABASES_TIDB_USER
    ZZT_API_KEY = zk_settings.ZZT_API_KEY
    ZZT_API_SECRET_KEY = zk_settings.ZZT_API_SECRET_KEY
    ZZT_DOMAIN_NAME = zk_settings.ZZT_DOMAIN_NAME
    CELERY_BROKER_URL = zk_settings.CELERY_BROKER_URL
    IDAAS_COMPANY_PUBLIC_KEY = zk_settings.IDAAS_COMPANY_PUBLIC_KEY
    IDAAS_COMPANY_PUBLIC_KEY_H5 = zk_settings.IDAAS_COMPANY_PUBLIC_KEY_H5
    SERVICE_CODE = zk_settings.SERVICE_CODE
    SERVICE_CODE_PWD = zk_settings.SERVICE_CODE_PWD
    TOKEN_URL = zk_settings.TOKEN_URL
    PROJECT_ID = zk_settings.PROJECT_ID
    PROJECT_SECRET = zk_settings.PROJECT_SECRET
    PERSON_CODE_APPLY_URL = zk_settings.PERSON_CODE_APPLY_URL
    PERSON_CODE_CHECK_URL = zk_settings.PERSON_CODE_CHECK_URL
    PERSON_CODE_INFO_URL = zk_settings.PERSON_CODE_INFO_URL
    ANALYSIS_MSG_WEBHOOK = zk_settings.ANALYSIS_MSG_WEBHOOK
    KIBANA_IP = zk_settings.KIBANA_IP
    KIBANA_PORT = zk_settings.KIBANA_PORT

    DATABASES["default"] = {
        "ENGINE": "django.db.backends.mysql",
        "NAME": "diagnosis",
        "USER": DATABASES_TIDB_USER,
        "PASSWORD": DATABASES_TIDB_PASSWORD,
        "HOST": DATABASES_TIDB_HOST,
        "PORT": DATABASES_TIDB_PORT,
        "OPTIONS": {"connect_timeout": 5},
    }

    JPUSH_APP_KEY = zk_settings.JPUSH_APP_KEY
    JPUSH_MASTER_SECRET = zk_settings.JPUSH_MASTER_SECRET
    PUSH_TAG = zk_settings.PUSH_TAG
    SHOW_SWAGGER_DOCS = DEBUG

    GOTENBERG_ADDR = zk_settings.GOTENBERG_ADDR

    OSS_ENDPOINT = zk_settings.OSS_ENDPOINT
    OSS_ACCESS_KEY_ID = zk_settings.OSS_ACCESS_KEY_ID
    OSS_ACCESS_KEY_SECRET = zk_settings.OSS_ACCESS_KEY_SECRET
    OSS_BUCKET = zk_settings.OSS_BUCKET
    OSS_TITLE_DIR = zk_settings.OSS_TITLE_DIR

    _redis_host = zk_settings.REDIS_HOST
    _redis_port = int(zk_settings.REDIS_PORT)
    if zk_settings.REDIS_PASSWORD == "None":
        _redis_password = None
    else:
        _redis_password = zk_settings.REDIS_PASSWORD

    REDIS = {"host": _redis_host, "port": _redis_port, "password": _redis_password}
    # BMOSS 地址
    if hasattr(zk_settings, "BMOSS_RPC_CHANNEL"):
        BMOSS_RPC_CHANNEL = zk_settings.BMOSS_RPC_CHANNEL

    GREEN_ACCESS_KEY_ID = zk_settings.GREEN_ACCESS_KEY_ID
    GREEN_ACCESS_KEY_SECRET = zk_settings.GREEN_ACCESS_KEY_SECRET
    NOTICE_APP_ID = zk_settings.NOTICE_APP_ID
    NOTICE_KEY_ID = zk_settings.NOTICE_KEY_ID
    NOTICE_SECRET_KEY = zk_settings.NOTICE_SECRET_KEY
