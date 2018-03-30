# -*- coding: utf-8 -*-
from opsweb import db_zeus


class DBZeusUserInfo(db_zeus.Model):
    __bind_key__ = 'zeus'
    __tablename__ = 'user_info'
    id = db_zeus.Column(db_zeus.Integer, primary_key=True, autoincrement=True)
    username = db_zeus.Column(db_zeus.String(255))
    role = db_zeus.Column(db_zeus.String(255))

    def __init__(self, username, role):
        self.username = username
        self.role = role
