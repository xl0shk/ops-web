# -*- coding: utf-8 -*-
from opsweb import db_zeus


class DBZeusProjectDeployTask(db_zeus.Model):
    __bind_key__ = 'zeus'
    __tablename__ = 'project_deploy_task'
    id = db_zeus.Column(db_zeus.Integer, primary_key=True, autoincrement=True)
    job_id = db_zeus.Column(db_zeus.Integer, db_zeus.ForeignKey('project_deploy_job.id'))
    project_id = db_zeus.Column(db_zeus.Integer, db_zeus.ForeignKey('project.id'))
    project_build_id = db_zeus.Column(db_zeus.Integer, db_zeus.ForeignKey('project_build.id'))
    env = db_zeus.Column(db_zeus.String(255))
    server_ip = db_zeus.Column(db_zeus.String(255))
    path = db_zeus.Column(db_zeus.String(255))
    deploy_done = db_zeus.Column(db_zeus.Integer)
    deploy_log = db_zeus.Column(db_zeus.Text)

    def __init__(self, job_id, project_id, project_build_id, env, server_ip, path, deploy_done, deploy_log):
        self.job_id = job_id
        self.project_id = project_id
        self.project_build_id = project_build_id
        self.env = env
        self.server_ip = server_ip
        self.path = path
        self.deploy_done = deploy_done
        self.deploy_log = deploy_log
