# -*- coding: utf-8 -*-
from opsweb import db_cmdb


class DBCmdbPhysicalServerProject(db_cmdb.Model):
    __bind_key__ = 'cmdb'
    __tablename__ = 'physical_server_project'
    id = db_cmdb.Column(db_cmdb.Integer, primary_key=True, autoincrement=True)
    physical_server_id = db_cmdb.Column(db_cmdb.Integer)
    physical_server_hostname = db_cmdb.Column(db_cmdb.String(255))
    project_id = db_cmdb.Column(db_cmdb.Integer)
    project_name = db_cmdb.Column(db_cmdb.String(255))

    def __init__(self, physical_server_id, physical_server_hostname, project_id, project_name):
        self.physical_server_id = physical_server_id
        self.physical_server_hostname = physical_server_hostname
        self.project_id = project_id
        self.project_name = project_name
