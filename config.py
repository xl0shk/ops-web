# -*- coding: utf-8 -*-


class Config(object):
    SECRET_KEY = 'aaaaaaaaxxxxxxxxxxxxxx'
    LOGPATH = "/data/logs/ops-web/stdout.log"
    LDAP_SERVER = '根据实际填写'
    LDAP_ADM_USER = '根据实际填写'
    LDAP_ADM_PSW = '根据实际填写'
    LDAP_PORT = 389
    LDAP_BASE_PATH = '根据实际填写'
    LDAP_DEFAULT_SEARCH_FILTER = '根据实际填写'
    LDAP_OBJECT_CLASS = '根据实际填写'
    CROWD_URL = '根据实际填写'
    CROWD_APP = '根据实际填写'
    CROWD_PSW = '根据实际填写'
    ZBX_ADMIN_USER = '根据实际填写'
    ZBX_ADMIN_PSW = '根据实际填写'
    ZBX_URL = '根据实际填写'
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    ES_CONFLUENCE_URL = '根据实际填写'

    IS_NOT_ADMIN = '只有管理员角色有操作权限'
    USER_LOGIN_ERROR = '用户名或密码不正确，请重新登录'
    USER_LOGIN_PRIVILEGE_ERROR = '没有登录权限'
    HAS_NO_PROJECT_PRIVILEGE = '没有项目权限'
    IS_NOT_AD_ADMIN = '您没有LDAP操作权限'
    IS_NOT_ZEUS_ADMIN = '您没有ZEUS操作权限'
    IS_NOT_CMDB_ADMIN = '您没有CMDB操作权限'
    DATA_EXIST = '数据已经存在'
    LDAP_REQUEST_ERROR = '与AD服务器的连接发生错误，LDAP请求失败'
    MYSQL_REQUEST_ERROR = '与MySQL服务器的连接发生错误，MySQL请求失败'
    IP_FORMAT_ERROR = 'IP地址格式不正确'

    @staticmethod
    def init_app(app):
        pass


class TestingConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://test:test@1.1.1.1/cmdb'
    SQLALCHEMY_BINDS = {'cmdb': 'mysql+pymysql://test:test@1.1.1.1/cmdb',
                        'zeus': 'mysql+pymysql://test:test@1.1.1.1/zeus'}


class PreReleaseConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://pre:pre@1.1.1.1/cmdb'
    SQLALCHEMY_BINDS = {'cmdb': 'mysql+pymysql://pre:pre@1.1.1.1/cmdb',
                        'zeus': 'mysql+pymysql://pre:pre@1.1.1.1/zeus'}


class ProductionConfig(Config):
    pass


config = {
    'testing': TestingConfig,
    'pre-release': PreReleaseConfig,
    'production': ProductionConfig
}
