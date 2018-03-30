# -*- coding: utf-8 -*-
from opsweb import db_zeus


class DBZeusProjectServer(db_zeus.Model):
    __bind_key__ = 'zeus'
    __tablename__ = 'project_server'
    id = db_zeus.Column(db_zeus.Integer, primary_key=True, autoincrement=True)
    project_id = db_zeus.Column(db_zeus.Integer, db_zeus.ForeignKey('project.id'))
    env = db_zeus.Column(db_zeus.String(255))
    server_ip = db_zeus.Column(db_zeus.String(255))
    path = db_zeus.Column(db_zeus.String(255))

    def __init__(self, project_id, env, server_ip, path):
        self.project_id = project_id
        self.env = env
        self.server_ip = server_ip
        self.path = path
