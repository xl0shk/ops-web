# -*- coding: utf-8 -*-
import datetime

from flask import render_template, request, redirect, url_for, current_app
from opsweb import db_cmdb
from flask_login import login_required, current_user

from opsweb.auth.admin import is_cmdb_admin
from opsweb.cmdb import cmdb
from opsweb.dao.db_cmdb_cloud_project import DBCmdbCloudProject
from opsweb.dao.db_cmdb_cloud_user import DBCmdbCloudUser
from opsweb.dao.db_cmdb_cloud_virtual_server import DBCmdbCloudVirtualServer
from opsweb.utils.ip_change import ip_str2Int


@cmdb.route('/server/cloudvps/list', methods=['GET'])
@login_required
def cmdb_server_cloudvps_list():
    username = current_user.name
    servers = DBCmdbCloudVirtualServer.query.filter_by().all()
    return render_template('cmdb_server_cloudvps_list.html', servers=servers)


@cmdb.route('/server/cloudvps/add', methods=['GET', 'POST'])
@login_required
@is_cmdb_admin
def cmdb_server_cloudvps_add():
    username = current_user.name
    if request.method == 'GET':
        return render_template('cmdb_server_cloudvps_add.html')
    if request.method == 'POST':
        hostname = request.form['hostname']
        cpu = request.form['cpu']
        create_time = datetime.datetime.now()
        memory = request.form['memory']
        disk = request.form['disk']
        wanip = request.form['wanip']
        wanip_alternate = ip_str2Int(wanip)
        lanip = request.form['lanip']
        os = request.form['os']
        os_version = request.form['os_version']
        broadband_type = request.form['broadband_type']
        remark = request.form['remark']
        location = request.form['location']
        group = request.form['group']

        server = DBCmdbCloudVirtualServer(hostname, create_time, cpu, memory, disk, wanip, wanip_alternate,
                                          broadband_type, lanip, os, os_version, location, group, remark)
        db_cmdb.session.add(server)
        db_cmdb.session.commit()
        return redirect(url_for("cmdb.cmdb_server_cloudvps_list"))
    return 'You should never reach here'


@cmdb.route('/server/cloudvps/edit', methods=['GET', 'POST'])
@login_required
@is_cmdb_admin
def cmdb_server_cloudvps_edit():
    username = current_user.name
    if request.method == 'GET':
        hostname = request.args.get('hostname')
        server = DBCmdbCloudVirtualServer.query.filter_by(hostname=hostname).first()
        return render_template('cmdb_server_cloudvps_edit.html', server=server)
    if request.method == 'POST':
        origin_hostname = request.form['origin_hostname']
        hostname = request.form['hostname']
        cpu = request.form['cpu']
        mem = request.form['memory']
        disk = request.form['disk']
        wanip = request.form['wanip']
        wanip_alternate = ip_str2Int(wanip)
        broadband_type = request.form['broadband_type']
        lanip = request.form['lanip']
        os = request.form['os']
        os_version = request.form['os_version']
        location = request.form['location']
        group = request.form['group']
        remark = request.form['remark']

        server = DBCmdbCloudVirtualServer.query.filter_by(hostname=origin_hostname).first()
        server.hostname = hostname
        server.cpu = cpu
        server.mem = mem
        server.disk = disk
        server.wanip = wanip
        server.wanip_alternate = wanip_alternate
        server.lanip = lanip
        server.broadband_type = broadband_type
        server.os = os
        server.os_version = os_version
        server.remark = remark
        server.location = location
        server.group = group
        db_cmdb.session.commit()
        return redirect(url_for("cmdb.cmdb_server_cloudvps_list"))
    return 'You should never reach here'


@cmdb.route('/server/cloudvps/detail', methods=['GET', 'POST'])
@login_required
@is_cmdb_admin
def cmdb_server_cloudvps_detail():
    username = current_user.name
    hostname = request.args.get('hostname')
    server = DBCmdbCloudVirtualServer.query.filter_by(hostname=hostname).first()
    return render_template('cmdb_server_cloudvps_detail.html', server=server)


@cmdb.route('/server/cloudvps/del', methods=['GET'])
@login_required
@is_cmdb_admin
def cmdb_server_cloudvps_del():
    username = current_user.name
    hostname = request.args.get('hostname')

    DBCmdbCloudVirtualServer.query.filter_by(hostname=hostname).delete()
    DBCmdbCloudUser.query.filter_by(cloud_vs_hostname=hostname).delete()
    DBCmdbCloudProject.query.filter_by(cloud_vs_hostname=hostname).delete()
    db_cmdb.session.commit()

    return redirect(url_for("cmdb.cmdb_server_cloudvps_list"))
