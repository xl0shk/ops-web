# -*- coding: utf-8 -*-
from flask import render_template, request, redirect, url_for, Blueprint, current_app
from opsweb import db_cmdb
from flask_login import login_required, current_user

from opsweb.cmdb import cmdb
from opsweb.dao.db_cmdb_cloud_project import DBCmdbCloudProject
from opsweb.dao.db_cmdb_kvm_project import DBCmdbKvmProject
from opsweb.dao.db_cmdb_physical_server_project import DBCmdbPhysicalServerProject
from opsweb.dao.db_cmdb_project import DBCmdbProject
from opsweb.auth.admin import is_cmdb_admin
import time

from opsweb.dao.db_cmdb_project_user import DBCmdbProjectUser


@cmdb.route('/project/list', methods=['GET'])
@login_required
def cmdb_project_list():
    projects = DBCmdbProject.query.all()
    return render_template('cmdb_project_list.html', projects=projects)


@cmdb.route('/project/add', methods=['GET', 'POST'])
@login_required
@is_cmdb_admin
def cmdb_project_add():
    if request.method == 'GET':
        return render_template('cmdb_project_add.html')
    if request.method == 'POST':
        name = request.form['name']
        group = request.form['group']
        port = request.form['port']
        port2 = request.form['port2']
        git_source = request.form['git_source']
        remark = request.form['remark']
        create_time = time.strftime('%Y-%m-%d %H:%M:%S')

        project = DBCmdbProject(name, create_time, git_source, group, port, port2, remark)
        db_cmdb.session.add(project)
        db_cmdb.session.commit()
        return redirect(url_for("cmdb.cmdb_project_list"))
    return None


@cmdb.route('/project/edit', methods=['GET', 'POST'])
@login_required
@is_cmdb_admin
def cmdb_project_edit():
    username = current_user.name
    if request.method == 'GET':
        project_id = int(request.args.get('projectId', '0'))
        project = DBCmdbProject.query.filter_by(id=project_id).first()
        current_app.logger.info('%s visit cmdb-project-edit page.', username)
        return render_template('cmdb_project_edit.html', project=project)
    if request.method == 'POST':
        project_id = request.form['projectId']
        name = request.form['name']
        group = request.form['group']
        port = request.form['port']
        remark = request.form['remark']

        project = DBCmdbProject.query.filter_by(id=project_id).first()
        project.name = name
        project.group = group
        project.port = port
        project.remark = remark
        db_cmdb.session.commit()
        return redirect(url_for("cmdb.cmdb_project_list"))
    return 'You should never reach here'


@cmdb.route('/project/del', methods=['GET'])
@login_required
@is_cmdb_admin
def cmdb_project_del():
    username = current_user.name
    project_id = int(request.args.get('projectId', '0'))

    DBCmdbProject.query.filter_by(id=project_id).delete()
    DBCmdbPhysicalServerProject.query.filter_by(project_id=project_id).delete()
    DBCmdbKvmProject.query.filter_by(project_id=project_id).delete()
    DBCmdbCloudProject.query.filter_by(project_id=project_id).delete()
    DBCmdbProjectUser.query.filter_by(project_id=project_id).delete()
    db_cmdb.session.commit()
    return redirect(url_for("cmdb.cmdb_project_list"))
