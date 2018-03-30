# -*- coding: utf-8 -*-
import datetime

from flask import render_template, request, redirect, url_for, Blueprint, current_app
from flask_login import login_required, current_user

from opsweb.auth.admin import is_cmdb_admin
from opsweb.cmdb import cmdb
from opsweb.dao.db_cmdb_cloud_user import DBCmdbCloudUser
from opsweb.dao.db_cmdb_kvm_user import DBCmdbKvmUser
from opsweb.dao.db_cmdb_physics_server_user import DBCmdbPhysicsServerUser
from opsweb.dao.db_cmdb_project_user import DBCmdbProjectUser
from opsweb.dao.db_cmdb_user import *


@cmdb.route('/user/list', methods=['GET'])
@login_required
def cmdb_user_list():
    username = current_user.name
    cmdb_users = DBCmdbUser.query.all()
    current_app.logger.info('%s visit cmdb-user-list page.', username)
    return render_template('cmdb_user_list.html', cmdb_users=cmdb_users)


@cmdb.route('/user/add', methods=['GET', 'POST'])
@login_required
@is_cmdb_admin
def cmdb_user_add():
    username = current_user.name
    if request.method == 'GET':
        current_app.logger.info('%s visit cmdb-user-add page.', username)
        return render_template('cmdb_user_add.html')
    if request.method == 'POST':
        name = request.form['name']
        create_time = datetime.datetime.now()
        realname = request.form['realname']
        cname = request.form['cname']
        email = request.form['email']
        phone = request.form['phone']
        remark = request.form['remark']
        ad_admin = int(request.form.get('adAdmin', 0))
        zeus_admin = int(request.form.get('zeusAdmin', 0))
        cmdb_admin = int(request.form.get('cmdbAdmin', 0))

        cmdb_user = DBCmdbUser(name, create_time, realname, cname, email, phone, ad_admin, zeus_admin, cmdb_admin,
                               remark)
        db_cmdb.session.add(cmdb_user)
        db_cmdb.session.commit()
        current_app.logger.info('%s success to add cmdb-user %s', username, name)
        return redirect(url_for("cmdb.cmdb_user_list"))
    return None


@cmdb.route('/user/edit', methods=['GET', 'POST'])
@login_required
@is_cmdb_admin
def cmdb_user_edit():
    username = current_user.name
    if request.method == 'GET':
        cmdb_user_id = int(request.args.get('cmdbUserId', '0'))
        cmdb_user = DBCmdbUser.query.filter_by(id=cmdb_user_id).first()
        current_app.logger.info('%s visit cmdb-user-edit page.', username)
        return render_template('cmdb_user_edit.html', cmdb_user=cmdb_user)
    if request.method == 'POST':
        cmdb_user_id = request.form['cmdbUserId']
        name = request.form['name']
        realname = request.form['realname']
        cname = request.form['cname']
        email = request.form['email']
        phone = request.form['phone']
        remark = request.form['remark']
        ad_admin = int(request.form.get('adAdmin', 0))
        zeus_admin = int(request.form.get('zeusAdmin', 0))
        cmdb_admin = int(request.form.get('cmdbAdmin', 0))

        current_app.logger.info('%s success to edit cmdb-user %s.', (username, name))
        cmdb_user = DBCmdbUser.query.filter_by(id=cmdb_user_id).first()
        cmdb_user.name = name
        cmdb_user.realname = realname
        cmdb_user.cname = cname
        cmdb_user.email = email
        cmdb_user.phone = phone
        cmdb_user.remark = remark
        cmdb_user.ad_admin = ad_admin
        cmdb_user.zeus_admin = zeus_admin
        cmdb_user.cmdb_admin = cmdb_admin
        db_cmdb.session.commit()
        return redirect(url_for("cmdb.cmdb_user_list"))
    return None


@cmdb.route('/user/del', methods=['GET'])
@login_required
@is_cmdb_admin
def cmdb_user_del():
    username = current_user.name
    cmdb_user_id = int(request.args.get('cmdbUserId', '0'))

    DBCmdbUser.query.filter_by(id=cmdb_user_id).delete()
    DBCmdbCloudUser.query.filter_by(cmdb_user_id=cmdb_user_id).delete()
    DBCmdbKvmUser.query.filter_by(cmdb_user_id=cmdb_user_id).delete()
    DBCmdbPhysicsServerUser.query.filter_by(cmdb_user_id=cmdb_user_id).delete()
    DBCmdbProjectUser.query.filter_by(cmdb_user_id=cmdb_user_id).delete()
    db_cmdb.session.commit()

    return redirect(url_for("cmdb.cmdb_user_list"))
