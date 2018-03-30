# -*- coding:utf-8 -*-
import crowd
from flask import current_app
"""
    如果username和password在crowd中验证成功，返回dict对象；如果验证失败，返回None；
    增加异常处理，如果建连失败，同样返回None。
"""


class Crowd(object):
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.crowd_url = current_app.config['CROWD_URL']
        self.crowd_app = current_app.config['CROWD_APP']
        self.crowd_psw = current_app.config['CROWD_PSW']

    def auth(self):
        try:
            crowd_conn = crowd.CrowdServer(self.crowd_url, self.crowd_app, self.crowd_psw)
            crowd_auth_result = crowd_conn.auth_user(self.username, self.password)
        except Exception as e:
            current_app.logger.exception('crowd connection error: '.format(e))
            return None
        else:
            return crowd_auth_result
