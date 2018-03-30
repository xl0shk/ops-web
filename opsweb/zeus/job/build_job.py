# -*- coding:utf-8 -*-
from opsweb.dao.db_zeus_project_build import *
from opsweb.dao.db_zeus_project import *
import subprocess
import os
from opsweb.zeus import zeus


def build_job(project, git_addr, branch, build_id, parent_project, build_type):
    with zeus.app_context():
        cmd = os.path.dirname(__file__) + '/../build/build.sh'
        p = subprocess.Popen([cmd, project, git_addr, branch, str(build_id), parent_project, build_type],
                             stdout=subprocess.PIPE,
                             stderr=subprocess.PIPE,
                             stdin=subprocess.PIPE)

        while True:
            stdout_line = p.stdout.readline()
            if not stdout_line:
                break
            stdout_line = stdout_line.decode('UTF-8')
            project_build_stdout = DBZeusProjectBuild.query.filter_by(id=build_id).first()
            project_build_stdout.build_log = project_build_stdout.build_log + stdout_line
            db_zeus.session.commit()
        while True:
            stderr_line = p.stderr.readline()
            if not stderr_line:
                break
            stderr_line = stderr_line.decode('UTF-8')
            project_build_stderr = DBZeusProjectBuild.query.filter_by(id=build_id).first()
            project_build_stderr.build_log = project_build_stderr.build_log + stderr_line
            db_zeus.session.commit()

        project_build = DBZeusProjectBuild.query.filter_by(id=build_id).first()
        project_build.build_done = 1
        db_zeus.session.commit()
