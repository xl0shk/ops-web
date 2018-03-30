# -*- coding:utf-8 -*-
from flask import render_template
from flask_login import login_required
from opsweb.dao.db_zeus_project_config import *
from opsweb.utils.user_zeus_privilege import *
from opsweb.dao.db_zeus_project import *
from opsweb.utils.check_privilege import *
from opsweb.zeus import zeus
from opsweb.auth.admin import is_zeus_admin


@zeus.route('/project/config/list', methods=['GET'])
@login_required
def zeus_project_config_list():
    email = current_user.email
    project_id = int(request.args.get('projectId', '0'))

    if has_project_privilege(email, project_id) is False:
        return redirect(url_for('zeus_project_config.zeus_project_list'))

    project = DBZeusProject.query.filter_by(id=project_id).first()
    test_configs = DBZeusProjectConfig.query.filter_by(project_id=project_id, env='test').all()
    pre_configs = DBZeusProjectConfig.query.filter_by(project_id=project_id, env='pre').all()
    online_configs = DBZeusProjectConfig.query.filter_by(project_id=project_id, env='online').all()

    return render_template('zeus_project_config_list.html', project=project, testConfigs=test_configs,
                           preConfigs=pre_configs, onlineConfigs=online_configs)


@zeus.route('/project/config/add', methods=['POST'])
@login_required
@is_zeus_admin
def zeus_project_config_add():
    project_id = int(request.form['projectId'])
    env = request.form['env']
    path = request.form['path']
    filename = request.form['filename']
    content = request.form['content']

    project_config = DBZeusProjectConfig(project_id, env, path, filename, content)
    db_cmdb.session.add(project_config)
    db_cmdb.session.commit()
    return redirect(url_for("zeus.zeus_project_config_list", projectId=project_id))


@zeus.route('/project/config/edit', methods=['GET', 'POST'])
@login_required
def zeus_project_config_edit():
    email = current_user.email
    if request.method == 'GET':
        config_id = int(request.args.get('id', '0'))
        project_config = DBZeusProjectConfig.query.filter_by(id=config_id).first()

        if has_project_privilege(email, project_config.project.id) is False:
            flash(current_app.config.get('HAS_NO_PROJECT_PRIVILEGE', 'alert'))
            return redirect(url_for('zeus.zeus_project_list'))

        return render_template('zeus_project_config_edit.html', config=project_config)

    if request.method == 'POST':
        config_id = int(request.form['id'])
        project_id = int(request.form['projectId'])
        content = request.form['content']

        project_config = DBZeusProjectConfig.query.filter_by(id=config_id).first()
        if is_zeus_admin(email) is False:
            flash(current_app.config.get('IS_NOT_ADMIN', 'alert'))
            return render_template('zeus_project_config_edit.html', config=project_config)

        project_config = DBZeusProjectConfig.query.filter_by(id=config_id).first()
        project_config.content = content
        db_zeus.session.commit()
        return redirect(url_for("zeus.zeus_project_config_list", projectId=project_id))

    return None


@zeus.route('/project/config/delete', methods=['GET'])
@login_required
@check_zeus_admin
def zeus_project_config_delete():
    config_id = int(request.args.get('id', '0'))
    project_id = int(request.args.get('projectId', '0'))

    project_config = DBZeusProjectConfig.query.filter_by(id=config_id).first()
    db_zeus.session.delete(project_config)
    db_zeus.session.commit()

    return redirect(url_for("zeus.zeus_project_config_list", projectId=project_id))
