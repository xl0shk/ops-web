# -*- coding: utf-8 -*-
from flask import render_template, request, redirect, url_for, flash, Blueprint, current_app
from flask_login import login_required, current_user
from opsweb.auth.admin import is_cmdb_admin
from opsweb.dao.db_cmdb_cloud_user import DBCmdbCloudUser
from opsweb.dao.db_cmdb_cloud_virtual_server import DBCmdbCloudVirtualServer
from opsweb.dao.db_cmdb_user import *
from . import cmdb


@cmdb.route('/cloud/privilege/list', methods=['GET'])
@login_required
def cmdb_cloud_privilege_list():
    username = current_user.name
    cloud_privileges = DBCmdbCloudUser.query.all()
    return render_template('cmdb_cloud_privilege_list.html', cloud_privileges=cloud_privileges)


@cmdb.route('/cloud/privilege/add', methods=['GET', 'POST'])
@login_required
@is_cmdb_admin
def cmdb_cloud_privilege_add():
    username = current_user.name
    if request.method == 'GET':
        servers = DBCmdbCloudVirtualServer.query.all()
        cmdb_users = DBCmdbUser.query.all()
        return render_template('cmdb_cloud_privilege_add.html', servers=servers, cmdb_users=cmdb_users)
    if request.method == 'POST':
        try:
            server_hostname = request.form['server_hostname']
            email = request.form['email']
            server = DBCmdbCloudVirtualServer.query.filter_by(hostname=server_hostname).first()
            cmdb_user = DBCmdbUser.query.filter_by(email=email).first()
            server_privilege = DBCmdbCloudUser(server.id, server.hostname, cmdb_user.id, cmdb_user.name,
                                               cmdb_user.cname)
            db_cmdb.session.add(server_privilege)
            db_cmdb.session.commit()
        except Exception as error:
            db_cmdb.session.rollback()
            flash(current_app.config['DATA_EXIST'], 'alert')
            return redirect(request.referrer)
        return redirect(url_for("cmdb.cmdb_cloud_privilege_list"))
    return None


@cmdb.route('/cloud/privilege/del', methods=['GET'])
@login_required
@is_cmdb_admin
def cmdb_cloud_privilege_del():
    username = current_user.name
    server_privilege_id = int(request.args.get('serverPrivilegeId', '0'))

    server_privilege = DBCmdbCloudUser.query.filter_by(id=server_privilege_id).first()
    db_cmdb.session.delete(server_privilege)
    db_cmdb.session.commit()

    return redirect(url_for("cmdb.cmdb_cloud_privilege_list"))
