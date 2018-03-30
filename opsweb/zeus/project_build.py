# -*- coding:utf-8 -*-
from flask import render_template, current_app
from flask_login import login_required, current_user
from opsweb.utils.user_zeus_privilege import *
from opsweb.utils.check_privilege import *
from opsweb.auth.admin import is_zeus_admin
from opsweb.zeus.job.build_job import *
import threading
import time
import json


@zeus.route('/project/build/list', methods=['GET'])
@login_required
def zeus_project_build_list():
    email = current_user.email
    project_id = int(request.args.get('projectId', '0'))

    if has_project_privilege(email, project_id) is False:
        return redirect(url_for('zeus_project_build.zeus_project_list'))

    project = DBZeusProject.query.filter_by(id=project_id).first()
    builds = DBZeusProjectBuild.query.filter_by(project_id=project.id).order_by(db_zeus.desc('id')).all()

    return render_template('zeus_project_build_list.html', project=project, builds=builds)


@zeus.route('/project/build/create', methods=['GET', 'POST'])
@login_required
def zeus_project_build_create():
    username = current_user.name
    email = current_user.email
    if request.method == 'GET':
        project_id = int(request.args.get('projectId', '0'))
        if has_project_privilege(email, project_id) is False:
            return redirect(url_for('zeus_project_build.zeus_project_list'))

        project = DBZeusProject.query.filter_by(id=project_id).first()
        return render_template('zeus_project_build_create.html', project=project)

    if request.method == 'POST':
        project_id = int(request.form.get('projectId', '0'))
        branch = request.form.get('branch')

        if has_project_privilege(email, project_id) is False:
            return redirect(url_for('zeus_project_build.zeus_project_list'))

        project = DBZeusProject.query.filter_by(id=project_id).first()
        build_id = int(time.strftime("%Y%m%d%H%M%S", time.localtime()))
        create_time = time.strftime('%Y-%m-%d %H:%M:%S')

        project_build = DBZeusProjectBuild(build_id, project_id, branch, 0, ' ', create_time)
        db_zeus.session.add(project_build)
        db_zeus.session.commit()

        t = threading.Thread(target=build_job, name='JobThread', args=(
            project.name, project.source, branch, build_id, project.parent_project, project.build_type))
        t.start()

        return '{"buildId" : ' + str(build_id) + '}'


@zeus.route('/project/build/view', methods=['GET'])
@login_required
def zeus_project_build_view():
    email = current_user.email
    build_id = int(request.args.get('buildId', '0'))
    project_build = DBZeusProjectBuild.query.filter_by(id=build_id).first()

    if has_project_privilege(email, project_build.project.id) is False:
        return redirect(url_for('zeus_project_build.zeus_project_list'))

    return render_template('zeus_project_build_view.html', build=project_build)


@zeus.route('/project/build/log', methods=['GET'])
@login_required
def zeus_project_build_log():
    build_id = int(request.args.get('id', '0'))
    project_build = DBZeusProjectBuild.query.filter_by(id=build_id).first()
    json_obj = {"done": project_build.build_done, "log": project_build.build_log}
    return json.dumps(json_obj)