# -*- coding:utf-8 -*-
from flask import render_template
from flask_login import login_required
from opsweb.dao.db_zeus_project import DBZeusProject
from opsweb.dao.db_zeus_project_config import DBZeusProjectConfig
from opsweb.utils.user_zeus_privilege import *
from opsweb.utils.check_privilege import *
import time
from opsweb.zeus import zeus
from opsweb.auth.admin import is_zeus_admin


@zeus.route('/project/list', methods=['GET'])
@login_required
def zeus_project_list():
    if current_user.zeus_admin == 1:
        projects = DBZeusProject.query.all()
    else:
        cmdb_user = DBCmdbUser.query.filter_by(email=current_user.email).first()
        user_info = DBCmdbProjectUser.query.filter_by(cmdb_user_id=cmdb_user.id).all()
        u_p_projectid = []
        for user in user_info:
            u_p_projectid.append(user.project_id)
        projects = DBZeusProject.query.filter(DBZeusProject.id.in_(u_p_projectid)).all()
    return render_template('zeus_project_list.html', projects=projects)


@zeus.route('/project/create', methods=['GET', 'POST'])
@login_required
@is_zeus_admin
def zeus_project_create():
    username = current_user.name
    if request.method == 'GET':
        current_app.logger.info('%s visit zeus-project-create page.', username)
        return render_template('zeus_project_create.html')

    if request.method == 'POST':
        project_name = request.values['projectName']
        cname = request.values['cname']
        git_url = request.values['gitUrl']
        parent_project = request.values['parentProject']
        build_type = request.values['buildType']
        startup_type = request.values['startupType']
        create_time = time.strftime('%Y-%m-%d %H:%M:%S')

        project = DBZeusProject(project_name, cname, git_url, parent_project, build_type, startup_type, create_time)
        db_cmdb.session.add(project)
        db_cmdb.session.commit()
        current_app.logger.info('%s success to create zeus project %s', (username, project_name))
        return redirect(url_for("zeus.zeus_project_list"))


@zeus.route('/project/edit', methods=['GET', 'POST'])
@login_required
@is_zeus_admin
def zeus_project_edit():
    username = current_user.name
    if request.method == 'GET':
        project_id = int(request.args.get('projectId', '0'))
        project = DBZeusProject.query.filter_by(id=project_id).first()
        current_app.logger.info('%s visit zeus-project-edit page.', username)
        return render_template('zeus_project_edit.html', project=project)

    if request.method == 'POST':
        project_id = int(request.form['id'])
        cname = request.form['cname']
        source = request.form['source']
        parent_project = request.form['parent_project']
        build_type = request.form['build_type']
        startup_type = request.form['startup_type']

        project = DBZeusProject.query.filter_by(id=project_id).first()
        project.cname = cname
        project.source = source
        project.parent_project = parent_project
        project.build_type = build_type
        project.startup_type = startup_type
        db_zeus.session.commit()
        return redirect(url_for("zeus.zeus_project_list"))
    return "Error method"


@zeus.route('/project/delete', methods=['GET'])
@login_required
@is_zeus_admin
def zeus_project_delete():
    username = current_user.id
    project_id = int(request.args.get('projectId', '0'))

    current_app.logger.info('%s success to delete zeus-project-id %s.', username, project_id)
    # 预删除相关表的数据
    DBZeusProjectConfig.query.filter_by(project_id=project_id).delete()
    db_zeus.session.commit()
    DBCmdbProjectUser.query.filter_by(project_id=project_id).delete()
    db_cmdb.session.commit()

    project = DBZeusProject.query.filter_by(id=project_id).first()
    db_zeus.session.delete(project)
    db_zeus.session.commit()

    return redirect(url_for('zeus.zeus_project_list'))
