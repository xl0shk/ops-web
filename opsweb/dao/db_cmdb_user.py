# -*- coding: utf-8 -*-
from flask_login import UserMixin
from .. import db_cmdb


class DBCmdbUser(db_cmdb.Model, UserMixin):
    __bind_key__ = 'cmdb'
    __tablename__ = 'cmdb_user'
    id = db_cmdb.Column(db_cmdb.Integer, primary_key=True, autoincrement=True)
    name = db_cmdb.Column(db_cmdb.String(255))
    create_time = db_cmdb.Column(db_cmdb.DateTime)
    realname = db_cmdb.Column(db_cmdb.String(255))
    cname = db_cmdb.Column(db_cmdb.String(255), index=True)
    email = db_cmdb.Column(db_cmdb.String(1024))
    phone = db_cmdb.Column(db_cmdb.String(255))
    ad_admin = db_cmdb.Column(db_cmdb.Integer)
    zeus_admin = db_cmdb.Column(db_cmdb.Integer)
    cmdb_admin = db_cmdb.Column(db_cmdb.Integer)
    remark = db_cmdb.Column(db_cmdb.String(255))

    def __init__(self, name, create_time, realname, cname, email, phone, ad_admin, zeus_admin, cmdb_admin, remark):
        self.name = name
        self.create_time = create_time
        self.realname = realname
        self.cname = cname
        self.email = email
        self.phone = phone
        self.ad_admin = ad_admin
        self.zeus_admin = zeus_admin
        self.cmdb_admin = cmdb_admin
        self.remark = remark
