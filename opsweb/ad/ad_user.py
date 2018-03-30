# -*- coding: utf-8 -*-
from flask import render_template, request, current_app, redirect, url_for, flash
from flask_login import login_required, current_user
from ..auth.admin import is_ad_admin
from .ldap_conn import LDAPConn
from ..ad import ad
from ..dao.db_cmdb_ad_user import DBCmdbADUser
from opsweb import db_cmdb
from ldap3 import MODIFY_REPLACE, MODIFY_ADD


@ad.route('/user/list', methods=['GET'])
@login_required
def ad_user_list():
    _ldap_base_path = current_app.config['LDAP_BASE_PATH'],
    _ldap_search_filter = current_app.config['LDAP_DEFAULT_SEARCH_FILTER']
    try:
        ldap_conn = LDAPConn()
        ldap_conn = ldap_conn.ldap_conn()
        ldap_conn.bind()
        ldap_conn.search(search_base=_ldap_base_path, search_filter=_ldap_search_filter, attributes=['*'])
        ad_users = ldap_conn.entries
    except Exception as e:
        current_app.logger.error('Error: {}'.format(e))
        flash(current_app.config['LDAP_REQUEST_ERROR'], 'alert')
        return redirect(request.referrer)
    else:
        ldap_conn.unbind()
        return render_template('ad_user_list.html', ad_users=ad_users)


@ad.route('/user/detail', methods=['GET'])
@login_required
def ad_user_detail():
    samaccountname = request.args.get('adUserId')
    search_filter = '(sAMAccountName=' + samaccountname + ')'
    _ldap_base_path = current_app.config['LDAP_BASE_PATH']
    try:
        ldap_conn = LDAPConn()
        ldap_conn = ldap_conn.ldap_conn()
        ldap_conn.bind()
        ldap_conn.search(search_base=_ldap_base_path, search_filter=search_filter, attributes=['*'])
        ad_user = ldap_conn.entries
        ad_user = ad_user[0]
    except Exception as e:
        current_app.logger.error('Error: {}'.format(e))
        flash(current_app.config['LDAP_REQUEST_ERROR'], 'alert')
        return redirect(request.referrer)
    else:
        ldap_conn.unbind()
        return render_template('ad_user_detail.html', ad_user=ad_user)


@ad.route('/user/add', methods=['GET', 'POST'])
@login_required
@is_ad_admin
def ad_user_add():
    if request.method == 'GET':
        return render_template('ad_user_add.html')
    if request.method == 'POST':
        display_name = request.form['displayName']
        cn = request.form['cn']
        sn = request.form['sn']
        given_name = request.form['givenName']
        s_am_account_name = request.form['sAMAccountName']
        department = request.form['department']
        title = request.form['title']
        user_account_control = request.form['userAccountControl']
        mail = request.form['mail']
        telephone_number = request.form['telephoneNumber']
        user_password = request.form['userPassword']
        groups = request.form.getlist('groups')

        _ldap_base_path = current_app.config['LDAP_BASE_PATH']
        dn = 'CN=' + cn + ',' + _ldap_base_path
        object_class = current_app.config.get('LDAP_OBJECT_CLASS')
        attributes = {'displayName': display_name, 'cn': cn, 'sn': sn, 'givenName': given_name,
                      'department': department, 'title': title, 'mail': mail, 'telephoneNumber': telephone_number,
                      'userAccountControl': user_account_control, 'sAMAccountName': s_am_account_name,
                      'userPassword': user_password}
        try:
            ldap_conn = LDAPConn()
            ldap_conn = ldap_conn.ldap_conn()
            ldap_conn.bind()
            ldap_conn.add(dn, object_class, attributes)
            for group_cn in groups:
                group_dn = 'CN=' + group_cn + ',' + _ldap_base_path
                group_change = {'member': [MODIFY_ADD, dn]}
                ldap_conn.modify(group_dn, group_change)
        except Exception as e:
            current_app.logger.error('Error: {}'.format(e))
            flash(current_app.config['LDAP_REQUEST_ERROR'], 'alert')
            return redirect(request.referrer)

        try:
            ad_user = DBCmdbADUser(cn, user_password)
            db_cmdb.session.add(ad_user)
            db_cmdb.session.commit()
        except Exception as e:
            current_app.logger.error('Error: {}'.format(e))
            flash(current_app.config['MYSQL_REQUEST_ERROR'], 'alert')
            return redirect(request.referrer)

        ldap_conn.unbind()
        return redirect(url_for("ad.ad_user_list"))


@ad.route('/user/edit', methods=['GET', 'POST'])
@login_required
@is_ad_admin
def ad_user_edit():
    if request.method == 'GET':
        samaccountname = request.args.get('adUserId')
        search_filter = '(sAMAccountName=' + samaccountname + ')'
        _ldap_base_path = current_app.config['LDAP_BASE_PATH']
        try:
            ldap_conn = LDAPConn()
            ldap_conn = ldap_conn.ldap_conn()
            ldap_conn.bind()
            ldap_conn.bind()
            ldap_conn.search(search_base=_ldap_base_path, search_filter=search_filter, attributes=['*'])
            ad_user = ldap_conn.entries
            ad_user = ad_user[0]
        except Exception as e:
            current_app.logger.error('Error: {}'.format(e))
            flash(current_app.config['LDAP_REQUEST_ERROR'], 'alert')
            return redirect(request.referrer)
        else:
            ldap_conn.unbind()
            return render_template('ad_user_edit.html', ad_user=ad_user)

    if request.method == 'POST':
        display_name = request.form['displayName']
        cn = request.form['cn']
        sn = request.form['sn']
        given_name = request.form['givenName']
        department = request.form['department']
        title = request.form['title']
        user_account_control = request.form['userAccountControl']
        mail = request.form['mail']
        telephone_number = request.form['telephoneNumber']

        _ldap_base_path = current_app.config['LDAP_BASE_PATH']
        dn = 'CN=' + cn + ',' + _ldap_base_path
        changes = {'displayName': [(MODIFY_REPLACE, display_name)], 'sn': [(MODIFY_REPLACE, sn)],
                   'givenName': [(MODIFY_REPLACE, given_name)], 'department': [(MODIFY_REPLACE, department)],
                   'title': [(MODIFY_REPLACE, title)], 'mail': [(MODIFY_REPLACE, mail)],
                   'telephoneNumber': [(MODIFY_REPLACE, telephone_number)],
                   'userAccountControl': [(MODIFY_REPLACE, user_account_control)]}

        try:
            ldap_conn = LDAPConn()
            ldap_conn = ldap_conn.ldap_conn()
            ldap_conn.bind()
            ldap_conn.modify(dn, changes)
        except Exception as e:
            current_app.logger.error('Error: {}'.format(e))
            flash(current_app.config['LDAP_REQUEST_ERROR'], 'alert')
            return redirect(request.referrer)
        else:
            ldap_conn.unbind()
            return redirect(url_for("ad.ad_user_list"))


@ad.route('/user/reset_pwd', methods=['GET', 'POST'])
@login_required
@is_ad_admin
def ad_user_reset_pwd():
    if request.method == 'GET':
        cn = request.args.get('cn')
        try:
            ad_user = DBCmdbADUser.query.filter_by(name=cn).first()
        except Exception as e:
            current_app.logger.error('Error: {}'.format(e))
            flash(current_app.config['MYSQL_REQUEST_ERROR'], 'alert')
            return redirect(request.referrer)
        else:
            return render_template('ad_user_reset_pwd.html', cn=cn, ad_user=ad_user)

    if request.method == 'POST':
        user_password = request.form['userPassword']
        cn = request.form['cn']

        _ldap_base_path = current_app.config.get('LDAP_BASE_PATH')
        dn = 'CN=' + cn + ',' + _ldap_base_path
        changes = {'userPassword': [(MODIFY_REPLACE, user_password)]}
        try:
            ldap_conn = LDAPConn()
            ldap_conn = ldap_conn.ldap_conn()
            ldap_conn.bind()
            ldap_conn.modify(dn, changes)
        except Exception as e:
            current_app.logger.error('Error: {}'.format(e))
            flash(current_app.config['LDAP_REQUEST_ERROR'], 'alert')
            return redirect(request.referrer)
        else:
            ldap_conn.unbind()
            return redirect(url_for("ad.ad_user_list"))


@ad.route('/user/del', methods=['GET'])
@login_required
@is_ad_admin
def ad_user_del():
    cn = request.args.get('cn')
    _ldap_base_path = current_app.config.get('LDAP_BASE_PATH')
    dn = 'CN=' + cn + ',' + _ldap_base_path
    try:
        ldap_conn = LDAPConn()
        ldap_conn = ldap_conn.ldap_conn()
        ldap_conn.bind()
        ldap_conn.delete(dn)
    except Exception as e:
        current_app.logger.error('Error: {}'.format(e))
        flash(current_app.config['LDAP_REQUEST_ERROR'], 'alert')
        return redirect(request.referrer)
    else:
        ldap_conn.unbind()
        return redirect(url_for("ad.ad_user_list"))
