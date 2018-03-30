# -*- coding:utf-8 -*-
from flask import render_template, current_app
from flask_login import login_required
from opsweb.dao.db_zeus_project_server import *
from opsweb.utils.user_zeus_privilege import *
from opsweb.dao.db_zeus_project import *
from opsweb.utils.check_privilege import *
from opsweb.auth.admin import is_zeus_admin
import re

from opsweb.zeus import zeus


@zeus.route('/project/server/list', methods=['GET'])
@login_required
def zeus_project_server_list():
    email = current_user.email
    project_id = int(request.args.get('projectId', '0'))
    project = DBZeusProject.query.filter_by(id=project_id).first()

    if has_project_privilege(email, project_id) is False:
        return redirect(url_for('zeus.zeus_project_list'))

    test_servers = DBZeusProjectServer.query.filter_by(project_id=project_id, env='test').all()
    pre_servers = DBZeusProjectServer.query.filter_by(project_id=project_id, env='pre').all()
    online_servers = DBZeusProjectServer.query.filter_by(project_id=project_id, env='online').all()

    return render_template('zeus_project_server_list.html', project=project, testServers=test_servers,
                           preServers=pre_servers, onlineServers=online_servers)


@zeus.route('/project/server/add', methods=['POST'])
@login_required
@is_zeus_admin
def project_server_add():
    username = current_user.name
    project_id = int(request.form['projectId'])
    env = request.form['env']
    ips = request.form['ips']
    path = request.form['path']

    ip_array = ips.split(",")
    for ip in ip_array:
        match = re.match("^(\d{1,3})\.(\d{1,3})\.(\d{1,3})\.(\d{1,3})$", ip)
        if not match:
            continue
        project_server = DBZeusProjectServer(project_id, env, ip, path)
        db_zeus.session.add(project_server)
        db_zeus.session.commit()

    return redirect(url_for("zeus.zeus_project_server_list", projectId=project_id))


@zeus.route('/project/server/delete', methods=['GET'])
@login_required
@check_zeus_admin
def zeus_project_server_delete():
    server_id = int(request.args.get('id', '0'))
    project_id = int(request.args.get('projectId', '0'))

    project_server = DBZeusProjectServer.query.filter_by(id=server_id).first()
    db_zeus.session.delete(project_server)
    db_zeus.session.commit()
    return redirect(url_for("zeus.zeus_project_server_list", projectId=project_id))
