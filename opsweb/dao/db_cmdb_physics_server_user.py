# -*- coding: utf-8 -*-
from opsweb import db_cmdb


class DBCmdbPhysicsServerUser(db_cmdb.Model):
    __bind_key__ = 'cmdb'
    __tablename__ = 'physical_server_cmdb_user'
    id = db_cmdb.Column(db_cmdb.Integer, primary_key=True, autoincrement=True)
    physical_server_id = db_cmdb.Column(db_cmdb.Integer)
    physical_server_hostname = db_cmdb.Column(db_cmdb.String(255))
    cmdb_user_id = db_cmdb.Column(db_cmdb.Integer)
    cmdb_user_name = db_cmdb.Column(db_cmdb.String(255))
    cmdb_user_cname = db_cmdb.Column(db_cmdb.String(255))

    def __init__(self, physical_server_id, physical_server_hostname, cmdb_user_id, cmdb_user_name, cmdb_user_cname):
        self.physical_server_id = physical_server_id
        self.physical_server_hostname = physical_server_hostname
        self.cmdb_user_id = cmdb_user_id
        self.cmdb_user_name = cmdb_user_name
        self.cmdb_user_cname = cmdb_user_cname
