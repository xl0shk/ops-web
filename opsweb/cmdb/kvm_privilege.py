# -*- coding: utf-8 -*-
import json

from flask import render_template, request, redirect, url_for, flash, current_app
from flask_login import login_required, current_user

from opsweb.auth.admin import is_cmdb_admin
from opsweb.cmdb import cmdb
from opsweb.dao.db_cmdb_kvm_user import DBCmdbKvmUser
from opsweb.dao.db_cmdb_kvm_virtual_server import DBCmdbKVMVirtualServer
from opsweb.dao.db_cmdb_user import *


@cmdb.route('/kvm/privilege/list', methods=['GET'])
@login_required
def cmdb_kvm_privilege_list():
    username = current_user.name
    kvm_privileges = DBCmdbKvmUser.query.all()
    return render_template('cmdb_kvm_privilege_list.html', kvm_privileges=kvm_privileges)


@cmdb.route('/kvm/privilege/add', methods=['GET', 'POST'])
@login_required
@is_cmdb_admin
def cmdb_kvm_privilege_add():
    username = current_user.name
    if request.method == 'GET':
        servers = DBCmdbKVMVirtualServer.query.all()
        cmdb_users = DBCmdbUser.query.all()
        current_app.logger.info('%s visit cmdb-server-privilege-add page.', username)
        return render_template('cmdb_kvm_privilege_add.html', servers=servers, cmdb_users=cmdb_users)
    if request.method == 'POST':
        try:
            server_hostname = request.form['server_hostname']
            email = request.form['email']
            server = DBCmdbKVMVirtualServer.query.filter_by(hostname=server_hostname).first()
            cmdb_user = DBCmdbUser.query.filter_by(email=email).first()
            server_privilege = DBCmdbKvmUser(server.id, server.hostname, cmdb_user.id, cmdb_user.name,
                                             cmdb_user.cname)
            db_cmdb.session.add(server_privilege)
            db_cmdb.session.commit()
        except Exception as error:
            db_cmdb.session.rollback()
            flash(current_app.config.get('DATA_EXIST'), 'alert')
            return redirect(request.referrer)
        return redirect(url_for("cmdb.cmdb_kvm_privilege_list"))
    return 'You should never reach here'


@cmdb.route('/kvm/privilege/del', methods=['GET'])
@login_required
@is_cmdb_admin
def cmdb_kvm_privilege_del():
    username = current_user.name
    server_privilege_id = int(request.args.get('serverPrivilegeId', '0'))

    server_privilege = DBCmdbKvmUser.query.filter_by(id=server_privilege_id).first()
    db_cmdb.session.delete(server_privilege)
    db_cmdb.session.commit()

    return redirect(url_for("cmdb.cmdb_kvm_privilege_list"))
