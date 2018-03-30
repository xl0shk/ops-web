# -*- coding: utf-8 -*-
from opsweb import db_cmdb


class DBCmdbCloudUser(db_cmdb.Model):
    __bind_key__ = 'cmdb'
    __tablename__ = 'cloud_vs_cmdb_user'
    id = db_cmdb.Column(db_cmdb.Integer, primary_key=True, autoincrement=True)
    cloud_vs_id = db_cmdb.Column(db_cmdb.Integer)
    cloud_vs_hostname = db_cmdb.Column(db_cmdb.String(255))
    cmdb_user_id = db_cmdb.Column(db_cmdb.Integer)
    cmdb_user_name = db_cmdb.Column(db_cmdb.String(255))
    cmdb_user_cname = db_cmdb.Column(db_cmdb.String(255))

    def __init__(self, cloud_vs_id, cloud_vs_hostname, cmdb_user_id, cmdb_user_name, cmdb_user_cname):
        self.cloud_vs_id = cloud_vs_id
        self.cloud_vs_hostname = cloud_vs_hostname
        self.cmdb_user_id = cmdb_user_id
        self.cmdb_user_name = cmdb_user_name
        self.cmdb_user_cname = cmdb_user_cname
