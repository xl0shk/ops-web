# -*- coding:utf-8 -*-
from opsweb.dao.db_zeus_project_deploy_task import *
import subprocess
import os
from opsweb.zeus import zeus


def deploy_job(task_id, project_name, build_id, server_ip, path, parent_project, startup_type):
    with zeus.app_context():
        cmd = os.path.dirname(__file__) + '/../deploy/deploy.sh'
        p = subprocess.Popen([cmd, project_name, str(build_id), server_ip, path, parent_project, startup_type],
                             stdout=subprocess.PIPE,
                             stderr=subprocess.PIPE,
                             stdin=subprocess.PIPE)
        # 捕获标准输出
        while True:
            stdout_line = p.stdout.readline()
            if not stdout_line:
                break
            stdout_line = stdout_line.decode('UTF-8')
            task_stdout = DBZeusProjectDeployTask.query.filter_by(id=task_id).first()
            task_stdout.deploy_log = task_stdout.deploy_log + stdout_line
            db_zeus.session.commit()
        # 捕获异常输出
        while True:
            stderr_line = p.stderr.readline()
            if not stderr_line:
                break
            stderr_line = stderr_line.decode('UTF-8')
            task_stderr = DBZeusProjectDeployTask.query.filter_by(id=task_id).first()
            task_stderr.deploy_log = task_stderr.deploy_log + stderr_line
            db_zeus.session.commit()

        project_deploy_task = DBZeusProjectDeployTask.query.filter_by(id=task_id).first()
        project_deploy_task.deploy_done = 1
        db_zeus.session.commit()
