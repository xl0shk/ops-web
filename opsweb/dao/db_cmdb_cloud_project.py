# -*- coding: utf-8 -*-
from opsweb import db_cmdb


class DBCmdbCloudProject(db_cmdb.Model):
    __bind_key__ = 'cmdb'
    __tablename__ = 'cloud_vs_project'
    id = db_cmdb.Column(db_cmdb.Integer, primary_key=True, autoincrement=True)
    cloud_vs_id = db_cmdb.Column(db_cmdb.Integer)
    cloud_vs_hostname = db_cmdb.Column(db_cmdb.String(255))
    project_id = db_cmdb.Column(db_cmdb.Integer)
    project_name = db_cmdb.Column(db_cmdb.String(255))

    def __init__(self, cloud_vs_id, cloud_vs_hostname, project_id, project_name):
        self.cloud_vs_id = cloud_vs_id
        self.cloud_vs_hostname = cloud_vs_hostname
        self.project_id = project_id
        self.project_name = project_name
