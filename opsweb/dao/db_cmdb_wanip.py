# -*- coding: utf-8 -*-
from opsweb import db_cmdb


class WanIP(db_cmdb.Model):
    __bind_key__ = 'cmdb'
    __tablename__ = 'wanip'
    id = db_cmdb.Column(db_cmdb.Integer, primary_key=True, autoincrement=True)
    ip = db_cmdb.Column(db_cmdb.String(255), index=True)
    broadband_type = db_cmdb.Column(db_cmdb.String(255))
    buy_time = db_cmdb.Column(db_cmdb.DateTime)
    mask = db_cmdb.Column(db_cmdb.String(255))
    gateway = db_cmdb.Column(db_cmdb.String(255))
    ip_range = db_cmdb.Column(db_cmdb.String(255))
    used = db_cmdb.Column(db_cmdb.Integer)
    hostname = db_cmdb.Column(db_cmdb.String(255))
    remark = db_cmdb.Column(db_cmdb.String(255))

    def __init__(self, ip, broadband_type, buy_time, mask, gateway, ip_range, used, hostname, remark):
        self.ip = ip
        self.broadband_type = broadband_type
        self.hostname = hostname
        self.buy_time = buy_time
        self.mask = mask
        self.gateway = gateway
        self.ip_range = ip_range
        self.used = used
        self.hostname = hostname
        self.remark = remark
