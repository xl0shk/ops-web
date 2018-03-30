# -*- coding: utf-8 -*-
from opsweb import db_cmdb


class DBCmdbProject(db_cmdb.Model):
    extend_existing = True
    __bind_key__ = 'cmdb'
    __tablename__ = 'project'
    id = db_cmdb.Column(db_cmdb.Integer, primary_key=True, autoincrement=True)
    name = db_cmdb.Column(db_cmdb.String(255), index=True)
    create_time = db_cmdb.Column(db_cmdb.DateTime)
    git_source = db_cmdb.Column(db_cmdb.String(255))
    group = db_cmdb.Column(db_cmdb.String(255))
    port = db_cmdb.Column(db_cmdb.Integer)
    port2 = db_cmdb.Column(db_cmdb.Integer)
    remark = db_cmdb.Column(db_cmdb.String(255))

    def __init__(self, name, create_time, git_source, group, port, port2, remark):
        self.name = name
        self.create_time = create_time
        self.git_source = git_source
        self.group = group
        self.port = port
        self.port2 = port2
        self.remark = remark
