# -*- coding:utf-8 -*-
from flask import url_for, redirect, flash, request, render_template
from flask_login import login_required
from opsweb.zeus import zeus
from opsweb.utils.check_privilege import *
from opsweb.auth.admin import is_zeus_admin


@zeus.route('/user/info', methods=['GET'])
@login_required
@check_zeus_admin
def zeus_user_info():
    user_infos = DBCmdbUser.query.all()
    return render_template('zeus_user_info.html', user_infos=user_infos)


@zeus.route('/user/info/edit', methods=['POST'])
@login_required
@check_zeus_admin
def zeus_user_info_add():
    email = request.form['email']
    role = request.form['userRole']
    user_info = DBCmdbUser.query.filter_by(email=email).first()
    user_info.zeus_admin = role
    db_cmdb.session.commit()
    return redirect(url_for("zeus.zeus_user_info"))


@zeus.route('/user/info/del', methods=['GET'])
@login_required
@check_zeus_admin
def zeus_user_info_del():
    user_info_id = int(request.args.get('id', '0'))
    user_info = DBZeusUserInfo.query.filter_by(id=user_info_id).first()
    db_cmdb.session.delete(user_info)
    db_cmdb.session.commit()
    return redirect(url_for("zeus.zeus_user_info"))
