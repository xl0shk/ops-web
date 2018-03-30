# -*- coding:utf-8 -*-
from flask import render_template, request, redirect, url_for
from .crowd import *
from .. import login_manager
from ..dao.db_cmdb_user import DBCmdbUser
from flask_login import login_user, login_required, logout_user
from . import auth


@login_manager.user_loader
def load_user(user_id):
    return DBCmdbUser.query.get(int(user_id))


@auth.route('/login', methods=['GET', 'POST'])
def login():
    error = ''
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        crowd_auth = Crowd(username, password).auth()
        if crowd_auth is not None:
            cmdb_user = DBCmdbUser.query.filter_by(name=username).first()
            if cmdb_user is None:
                error = current_app.config['USER_LOGIN_PRIVILEGE_ERROR']
                return render_template('login.html', error=error)
            login_user(cmdb_user)
            next_url = request.args.get('next')
            return redirect(next_url or url_for('views.index'))
        else:
            error = ""
    return render_template('login.html', error=error)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))
