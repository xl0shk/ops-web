# -*- coding:utf-8 -*-
from flask import render_template, url_for, redirect, flash, request, Blueprint
from flask_login import login_required, current_user

from opsweb.cmdb import cmdb
from opsweb.utils.user_zeus_privilege import *
from opsweb.dao.db_zeus_project import *
from opsweb.utils.check_privilege import *


@cmdb.route('/user/privilege/list', methods=['GET'])
@login_required
@check_zeus_admin
def zeus_user_privilege():
    project_users = DBCmdbProjectUser.query.all()
    projects = DBZeusProject.query.all()
    users = DBCmdbUser.query.all()

    return render_template('zeus_user_privilege.html', project_users=project_users, projects=projects, users=users)


@cmdb.route('/user/privilege/add', methods=['POST'])
@login_required
@check_zeus_admin
def admin_user_privilege_add():
    email = request.form['email']
    project_name = request.form['projectName']

    user = DBCmdbUser.query.filter_by(email=email).first()
    project = DBZeusProject.query.filter_by(name=project_name).first()
    # TODO:增加project为空的判断
    try:
        user_privilege = DBCmdbProjectUser(project.id, project.name, user.id, user.name, user.cname)
        db_cmdb.session.add(user_privilege)
        db_cmdb.session.commit()
    except Exception as e:
        db_cmdb.session.rollback()
        flash(current_app.config['DATA_EXIST'], 'alert')
        return redirect(request.referrer)
    return redirect(url_for("cmdb.zeus_user_privilege"))


# todo 删除编辑按钮
@cmdb.route('/user/privilege/edit', methods=['GET', 'POST'])
@login_required
@check_zeus_admin
def zeus_user_privilege_edit():
    if request.method == 'GET':
        user_privilege_id = int(request.args.get('id', '0'))
        user_privilege = DBCmdbProjectUser.query.filter_by(id=user_privilege_id).first()
        return render_template('zeus_user_privilege_edit.html', user_privilege=user_privilege)

    if request.method == 'POST':
        user_privilege_id = int(request.form['id'])
        user_id = request.form['userId']
        project_id = request.form['userId']

        user_info = DBCmdbUser.query.filter_by(id=user_id).first()
        project = DBZeusProject.query.filter_by(id=project_id).first()
        user_privilege = DBCmdbProjectUser.query.filter_by(id=user_privilege_id).first()
        user_privilege.user_id = user_info.id
        user_privilege.project_id = project.id
        user_privilege.project_name = project.project_name
        db_cmdb.session.commit()
        return redirect(url_for("cmdb.zeus_user_privilege"))

    return "Error method."


@cmdb.route('/user/privilege/del', methods=['GET'])
@login_required
@check_zeus_admin
def zeus_user_privilege_del():
    user_privilege_id = int(request.args.get('id', '0'))
    user_privilege = DBCmdbProjectUser.query.filter_by(id=user_privilege_id).first()
    db_cmdb.session.delete(user_privilege)
    db_cmdb.session.commit()
    return redirect(url_for("cmdb.zeus_user_privilege"))
