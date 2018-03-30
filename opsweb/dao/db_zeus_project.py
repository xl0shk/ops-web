# -*- coding: utf-8 -*-
from opsweb import db_zeus


class DBZeusProject(db_zeus.Model):
    extend_existing = True
    __bind_key__ = 'zeus'
    __tablename__ = 'project'
    id = db_zeus.Column(db_zeus.Integer, primary_key=True, autoincrement=True)
    name = db_zeus.Column(db_zeus.String(255))
    cname = db_zeus.Column(db_zeus.String(255))
    source = db_zeus.Column(db_zeus.String(1024))
    parent_project = db_zeus.Column(db_zeus.String(255))
    build_type = db_zeus.Column(db_zeus.String(255))
    startup_type = db_zeus.Column(db_zeus.String(255))
    create_time = db_zeus.Column(db_zeus.DateTime)

    def __init__(self, name, cname, source, parent_project, build_type, startup_type, create_time):
        self.name = name
        self.cname = cname
        self.source = source
        self.parent_project = parent_project
        self.build_type = build_type
        self.startup_type = startup_type
        self.create_time = create_time
