# -*- coding: utf-8 -*-
from opsweb import db_cmdb


class DBCmdbKvmUser(db_cmdb.Model):
    __bind_key__ = 'cmdb'
    __tablename__ = 'kvm_vs_cmdb_user'
    id = db_cmdb.Column(db_cmdb.Integer, primary_key=True, autoincrement=True)
    kvm_vs_id = db_cmdb.Column(db_cmdb.Integer)
    kvm_vs_hostname = db_cmdb.Column(db_cmdb.String(255))
    cmdb_user_id = db_cmdb.Column(db_cmdb.Integer)
    cmdb_user_name = db_cmdb.Column(db_cmdb.String(255))
    cmdb_user_cname = db_cmdb.Column(db_cmdb.String(255))

    def __init__(self, kvm_vs_id, kvm_vs_hostname, cmdb_user_id, cmdb_user_name, cmdb_user_cname):
        self.kvm_vs_id = kvm_vs_id
        self.kvm_vs_hostname = kvm_vs_hostname
        self.cmdb_user_id = cmdb_user_id
        self.cmdb_user_name = cmdb_user_name
        self.cmdb_user_cname = cmdb_user_cname
