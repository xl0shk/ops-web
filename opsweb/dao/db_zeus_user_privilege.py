# -*- coding: utf-8 -*-
from opsweb import db_zeus


class DBZeusUserPrivilege(db_zeus.Model):
    __bind_key__ = 'zeus'
    __tablename__ = 'user_privilege'
    id = db_zeus.Column(db_zeus.Integer, primary_key=True, autoincrement=True)
    user_id = db_zeus.Column(db_zeus.Integer, db_zeus.ForeignKey('user_info.id'))
    project_id = db_zeus.Column(db_zeus.Integer, db_zeus.ForeignKey('project.id'))
    project_name = db_zeus.Column(db_zeus.String(255))

    def __init__(self, user_id, project_id, project_name):
        self.user_id = user_id
        self.project_id = project_id
        self.project_name = project_name
