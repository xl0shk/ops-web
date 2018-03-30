# -*- coding: utf-8 -*-
from opsweb import db_cmdb


class DBCmdbADUser(db_cmdb.Model):
    __bind_key__ = 'cmdb'
    __tablename__ = 'ad_user'
    id = db_cmdb.Column(db_cmdb.Integer, primary_key=True, autoincrement=True)
    name = db_cmdb.Column(db_cmdb.String(255))
    initial_pwd = db_cmdb.Column(db_cmdb.String(255))

    def __init__(self, name, initial_pwd):
        self.name = name
        self.initial_pwd = initial_pwd
