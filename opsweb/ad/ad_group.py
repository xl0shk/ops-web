# -*- coding: utf-8 -*-
from flask import render_template, current_app, request, redirect, url_for, flash
from ldap3 import MODIFY_ADD, MODIFY_DELETE
from flask_login import login_required, current_user
from .ldap_conn import LDAPConn
from ..ad import ad
from ..auth.admin import is_ad_admin


@ad.route('/group/list', methods=['GET'])
@login_required
def ad_group_list():
    search_filter = '(objectClass=group)'
    _ldap_base_path = current_app.config['LDAP_BASE_PATH']
    try:
        ldap_conn = LDAPConn()
        ldap_conn = ldap_conn.ldap_conn()
        ldap_conn.bind()
        ldap_conn.search(search_base=_ldap_base_path, search_filter=search_filter, attributes=['*'])
        ad_groups = ldap_conn.entries
    except Exception as e:
        current_app.logger.error('Error: {}'.format(e))
        flash(current_app.config['LDAP_REQUEST_ERROR'], 'alert')
        return redirect(request.referrer)
    else:
        ldap_conn.unbind()
        return render_template('ad_group_list.html', ad_groups=ad_groups)


@ad.route('/group/member/list', methods=['GET'])
@login_required
@is_ad_admin
def ad_group_member_list():
    group_cn = request.args.get('groupCN')
    search_filter = '(cn=' + group_cn + ')'
    _ldap_base_path = current_app.config['LDAP_BASE_PATH']
    try:
        ldap_conn = LDAPConn()
        ldap_conn = ldap_conn.ldap_conn()
        ldap_conn.bind()
        ldap_conn.search(search_base=_ldap_base_path, search_filter=search_filter, attributes=['*'])
        ad_group = ldap_conn.entries
        group = ad_group[0]
    except Exception as e:
        current_app.logger.error('Error: {}'.format(e))
        flash(current_app.config['LDAP_REQUEST_ERROR'], 'alert')
        return redirect(request.referrer)
    else:
        ldap_conn.unbind()
        return render_template('ad_group_member_list.html', members=group.member, group_cn=group_cn)


@ad.route('/group/member/add', methods=['GET', 'POST'])
@login_required
@is_ad_admin
def ad_group_member_add():
    if request.method == 'GET':
        group_cn = request.args.get('groupCN')
        return render_template('ad_group_member_add.html', group_cn=group_cn)
    if request.method == 'POST':
        member = request.form['member']
        group_cn = request.form['groupCN']
        _ldap_base_path = current_app.config['LDAP_BASE_PATH']
        dn = 'CN=' + member + ',' + _ldap_base_path
        group_dn = 'CN=' + group_cn + ',' + _ldap_base_path
        group_change = {'member': [MODIFY_ADD, dn]}
        try:
            ldap_conn = LDAPConn()
            ldap_conn = ldap_conn.ldap_conn()
            ldap_conn.bind()
            ldap_conn.modify(group_dn, group_change)
        except Exception as e:
            current_app.logger.error('Error: {}'.format(e))
            flash(current_app.config['LDAP_REQUEST_ERROR'], 'alert')
            return redirect(request.referrer)
        else:
            ldap_conn.unbind()
            return redirect(url_for("ad.ad_group_member_list", groupCN=group_cn))


@ad.route('/group/member/del', methods=['GET'])
@login_required
@is_ad_admin
def ad_group_member_del():
    group_cn = request.args.get('groupCN')
    member_dn = request.args.get('member')
    _ldap_base_path = current_app.config['LDAP_BASE_PATH']
    group_dn = 'CN=' + group_cn + ',' + _ldap_base_path
    group_change = {'member': [MODIFY_DELETE, member_dn]}
    try:
        ldap_conn = LDAPConn()
        ldap_conn = ldap_conn.ldap_conn()
        ldap_conn.bind()
        ldap_conn.modify(group_dn, group_change)
    except Exception as e:
        current_app.logger.error('Error: {}'.format(e))
        flash(current_app.config['LDAP_REQUEST_ERROR'], 'alert')
        return redirect(request.referrer)
    else:
        ldap_conn.unbind()
        return redirect(url_for("ad.ad_group_member_list", groupCN=group_cn))
