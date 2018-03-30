# -*- coding: utf-8 -*-
from opsweb import db_zeus


class DBZeusProjectBuild(db_zeus.Model):
    __bind_key__ = 'zeus'
    __tablename__ = 'project_build'
    id = db_zeus.Column(db_zeus.Integer, primary_key=True)
    project_id = db_zeus.Column(db_zeus.Integer, db_zeus.ForeignKey('project.id'))
    branch = db_zeus.Column(db_zeus.String(255))
    build_done = db_zeus.Column(db_zeus.Integer)
    build_log = db_zeus.Column(db_zeus.Text)
    create_time = db_zeus.Column(db_zeus.DateTime)

    def __init__(self, build_id, project_id, branch, build_done, build_log, create_time):
        self.id = build_id
        self.project_id = project_id
        self.branch = branch
        self.build_done = build_done
        self.build_log = build_log
        self.create_time = create_time
