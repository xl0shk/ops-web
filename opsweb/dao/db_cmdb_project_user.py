# -*- coding: utf-8 -*-
from opsweb import db_cmdb


class DBCmdbProjectUser(db_cmdb.Model):
    __bind_key__ = 'cmdb'
    __tablename__ = 'project_cmdb_user'
    id = db_cmdb.Column(db_cmdb.Integer, primary_key=True, autoincrement=True)
    project_id = db_cmdb.Column(db_cmdb.Integer)
    project_name = db_cmdb.Column(db_cmdb.String(255))
    cmdb_user_id = db_cmdb.Column(db_cmdb.Integer)
    cmdb_user_name = db_cmdb.Column(db_cmdb.String(255))
    cmdb_user_cname = db_cmdb.Column(db_cmdb.String(255))

    def __init__(self, project_id, project_name, cmdb_user_id, cmdb_user_name, cmdb_user_cname):
        self.project_id = project_id
        self.project_name = project_name
        self.cmdb_user_id = cmdb_user_id
        self.cmdb_user_name = cmdb_user_name
        self.cmdb_user_cname = cmdb_user_cname
