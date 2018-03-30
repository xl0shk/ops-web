# -*- coding: utf-8 -*-
from opsweb import db_zeus


class DBZeusProjectDeployJob(db_zeus.Model):
    __bind_key__ = 'zeus'
    __tablename__ = 'project_deploy_job'
    id = db_zeus.Column(db_zeus.Integer, primary_key=True, autoincrement=True)
    project_id = db_zeus.Column(db_zeus.Integer, db_zeus.ForeignKey('project.id'))
    project_build_id = db_zeus.Column(db_zeus.Integer, db_zeus.ForeignKey('project_build.id'))
    task_num = db_zeus.Column(db_zeus.Integer)
    create_time = db_zeus.Column(db_zeus.DateTime)

    def __init__(self, job_id, project_id, project_build_id, task_num, create_time):
        self.id = job_id
        self.project_id = project_id
        self.project_build_id = project_build_id
        self.task_num = task_num
        self.create_time = create_time
