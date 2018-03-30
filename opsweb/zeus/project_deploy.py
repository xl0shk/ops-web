# -*- coding:utf-8 -*-
from flask import render_template, request, redirect, url_for, current_app
from flask_login import login_required, current_user
from opsweb.dao.db_zeus_project_deploy_job import DBZeusProjectDeployJob
from opsweb.dao.db_zeus_project_server import *
from opsweb.dao.db_zeus_project_config import *
from opsweb.dao.db_zeus_project_build import *
from opsweb.dao.db_zeus_project import *
from opsweb.utils.user_zeus_privilege import *
from opsweb.zeus.job.deploy_job import *
from opsweb.auth.admin import is_zeus_admin
from sqlalchemy import desc
import threading
import time
import json


@zeus.route('/project/deploy/deploy', methods=['GET'])
@login_required
def zeus_project_deploy_deploy():
    email = current_user.email
    build_id = int(request.values['buildId'])
    project_build = DBZeusProjectBuild.query.filter_by(id=build_id).first()

    if has_project_privilege(email, project_build.project.id) is False:
        return redirect(url_for('zeus.zeus_project_build_view', buildId=build_id))

    test_deploy_info = DBZeusProjectServer.query.filter_by(project_id=project_build.project.id, env='test').all()
    pre_deploy_info = DBZeusProjectServer.query.filter_by(project_id=project_build.project.id, env='pre').all()
    online_deploy_info = DBZeusProjectServer.query.filter_by(project_id=project_build.project.id, env='online').all()
    return render_template('zeus_project_deploy_deploy.html', test_deployinfo=test_deploy_info,
                           pre_deployinfo=pre_deploy_info, online_deployinfo=online_deploy_info, build=project_build)


@zeus.route('/project/deploy/action', methods=['POST'])
@login_required
def zeus_project_deploy_action():
    email = current_user.email
    build_id = request.values['buildId']
    project_server_ids = request.values['projectServerIds']
    env = request.values['env']

    project_build = DBZeusProjectBuild.query.filter_by(id=build_id).first()
    project = DBZeusProject.query.filter_by(id=project_build.project_id).first()

    if has_project_privilege(email, project.id) is False:
        return redirect(url_for('zeus.project_deploy_deploy', buildId=build_id))
    project_server_id_array = project_server_ids.split(",")
    task_num = len(project_server_id_array)
    job_id = int(time.strftime("%Y%m%d%H%M%S", time.localtime()))
    create_time = time.strftime('%Y-%m-%d %H:%M:%S')

    project_deploy_job = DBZeusProjectDeployJob(job_id, project.id, build_id, task_num, create_time)
    db_zeus.session.add(project_deploy_job)
    db_zeus.session.commit()

    # 在执行部署脚本之前，进行配置文件的替换
    configs = DBZeusProjectConfig.query.filter_by(project_id=project.id, env=env).all()
    if project.parent_project == "":
        project_path = '/data/zeus/build/%s/%s/dist/%s' % (build_id, project.name, project.name)
    else:
        project_path = '/data/zeus/build/%s/%s/%s/dist/%s' % (
            build_id, project.parent_project, project.name, project.name)
    for config in configs:
        config_path = project_path + config.path + '/' + config.filename
        file_object = open(config_path, 'w')
        file_object.write(config.content)
        file_object.close()

    # 每个服务器ip都执行一个task id
    for project_server_id in project_server_id_array:
        project_server = DBZeusProjectServer.query.filter_by(id=project_server_id).first()
        project_deploy_task = DBZeusProjectDeployTask(job_id, project.id, project_build.id, project_server.env,
                                                      project_server.server_ip, project_server.path, 0, '')
        db_zeus.session.add(project_deploy_task)
        db_zeus.session.flush()
        task_id = project_deploy_task.id
        db_zeus.session.commit()

        # 启动线程执行deploy任务
        t = threading.Thread(target=deploy_job, name='JobThread', args=(
            task_id, project.name, build_id, project_server.server_ip, project_server.path, project.parent_project,
            project.startup_type))
        t.start()

    return '{"jobId" : ' + str(job_id) + '}'


@zeus.route('/project/deploy/jobstatus', methods=['GET'])
def zeus_project_deploy_jobstatus():
    build_id = request.values['buildId']
    tasks_t = DBZeusProjectDeployTask.query.filter_by(project_build_id=build_id).order_by(
        desc(DBZeusProjectDeployTask.id)).all()
    tasks = []
    # remove _sa_instance_state from dict
    for task in tasks_t:
        task.__dict__.pop('_sa_instance_state', None)
        tasks.append(task.__dict__)
    return json.dumps(tasks)


@zeus.route('/project/deploy/log', methods=['GET'])
def zeus_project_deploy_log():
    task_id = request.values['taskId']
    task = DBZeusProjectDeployTask.query.filter_by(id=task_id).first()
    return render_template('zeus_project_deploy_log.html', task=task)


@zeus.route('/project/deploy/log_roll', methods=['GET'])
def zeus_project_deploy_log_roll():
    task_id = request.values['taskId']
    task = DBZeusProjectDeployTask.query.filter_by(id=task_id).first()
    task.__dict__.pop('_sa_instance_state', None)
    return json.dumps(task.__dict__)
