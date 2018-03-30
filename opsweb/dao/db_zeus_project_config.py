# -*- coding: utf-8 -*-
from opsweb import db_zeus


class DBZeusProjectConfig(db_zeus.Model):
    __bind_key__ = 'zeus'
    __tablename__ = 'project_config'
    id = db_zeus.Column(db_zeus.Integer, primary_key=True, autoincrement=True)
    project_id = db_zeus.Column(db_zeus.Integer, db_zeus.ForeignKey('project.id'))
    env = db_zeus.Column(db_zeus.String(255))
    path = db_zeus.Column(db_zeus.String(255))
    filename = db_zeus.Column(db_zeus.String(255))
    content = db_zeus.Column(db_zeus.Text)

    def __init__(self, project_id, env, path, filename, content):
        self.project_id = project_id
        self.env = env
        self.path = path
        self.filename = filename
        self.content = content
