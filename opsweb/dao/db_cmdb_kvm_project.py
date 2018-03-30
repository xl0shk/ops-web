# -*- coding: utf-8 -*-
from opsweb import db_cmdb


class DBCmdbKvmProject(db_cmdb.Model):
    __bind_key__ = 'cmdb'
    __tablename__ = 'kvm_vs_project'
    id = db_cmdb.Column(db_cmdb.Integer, primary_key=True, autoincrement=True)
    kvm_vs_id = db_cmdb.Column(db_cmdb.Integer)
    kvm_vs_hostname = db_cmdb.Column(db_cmdb.String(255))
    project_id = db_cmdb.Column(db_cmdb.Integer)
    project_name = db_cmdb.Column(db_cmdb.String(255))

    def __init__(self, kvm_vs_id, kvm_vs_hostname, project_id, project_name):
        self.kvm_vs_id = kvm_vs_id
        self.kvm_vs_hostname = kvm_vs_hostname
        self.project_id = project_id
        self.project_name = project_name
