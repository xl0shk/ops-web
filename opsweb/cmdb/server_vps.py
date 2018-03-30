# -*- coding: utf-8 -*-
import datetime
from flask import render_template, request, redirect, url_for, current_app, flash
from opsweb import db_cmdb
from flask_login import login_required, current_user
from ..auth.admin import is_cmdb_admin
from ..cmdb import cmdb
from ..dao.db_cmdb_kvm_project import DBCmdbKvmProject
from ..dao.db_cmdb_kvm_user import DBCmdbKvmUser
from ..dao.db_cmdb_kvm_virtual_server import DBCmdbKVMVirtualServer
from ..utils.validate_ip import validate_ip


@cmdb.route('/server/vps/list', methods=['GET'])
@login_required
def cmdb_server_vps_list():
    try:
        servers = DBCmdbKVMVirtualServer.query.filter_by().all()
    except Exception as e:
        current_app.logger.error('Error: {}'.format(e))
        flash(current_app.config['MYSQL_REQUEST_ERROR'], 'alert')
        return redirect(request.referrer)
    else:
        return render_template('cmdb_server_vps_list.html', servers=servers)


@cmdb.route('/server/vps/add', methods=['GET', 'POST'])
@login_required
@is_cmdb_admin
def cmdb_server_vps_add():
    if request.method == 'GET':
        return render_template('cmdb_server_vps_add.html')

    if request.method == 'POST':
        hostname = request.form.get('hostname')
        cpu = int(request.form.get('cpu')) if request.form.get('cpu') != '' else 0
        memory = int(request.form.get('memory')) if request.form.get('memory') != '' else 0
        disk = int(request.form.get('disk')) if request.form.get('disk') != '' else 0
        wanip = request.form.get('wanip')
        wanip_alternate = request.form.get('wanip_alternate')
        broadband_type = request.form.get('broadband_type')
        lanip = request.form.get('lanip')
        os = request.form.get('os')
        os_version = request.form.get('os_version')
        kvm_host = request.form.get('kvm_host')
        kvm_cpu_bind = request.form.get('kvm_cpu_bind')
        kvm_vnc_ip = request.form.get('kvm_vnc_ip')
        kvm_vnc_port = request.form.get('kvm_vnc_port')
        location = request.form.get('location')
        group = request.form.get('group')
        remark = request.form.get('remark')

        create_time = datetime.datetime.now()
        for ip in [wanip, wanip_alternate, lanip, kvm_vnc_ip]:
            if ip != '' and validate_ip(ip) is False:
                current_app.logger.error('warning: {} format error.'.format(ip))
                flash('{} {}'.format(ip, current_app.config['IP_FORMAT_ERROR']), 'alert')
                return redirect(request.referrer)

        try:
            server = DBCmdbKVMVirtualServer(hostname, create_time, cpu, memory, disk, wanip, wanip_alternate,
                                            broadband_type, lanip, os, os_version,
                                            kvm_host, kvm_cpu_bind, kvm_vnc_ip, kvm_vnc_port, location, group, remark)
            db_cmdb.session.add(server)
            db_cmdb.session.commit()
        except Exception as e:
            current_app.logger.error('Error: {}'.format(e))
            flash(current_app.config['MYSQL_REQUEST_ERROR'], 'alert')
            return redirect(request.referrer)
        else:
            return redirect(url_for("cmdb.cmdb_server_vps_list"))
    return None


@cmdb.route('/server/vps/edit', methods=['GET', 'POST'])
@login_required
@is_cmdb_admin
def cmdb_server_vps_edit():
    username = current_user.name
    if request.method == 'GET':
        hostname = request.args.get('hostname')
        server = DBCmdbKVMVirtualServer.query.filter_by(hostname=hostname).first()
        return render_template('cmdb_server_vps_edit.html', server=server)
    if request.method == 'POST':
        origin_hostname = request.form['origin_hostname']
        hostname = request.form['hostname']
        cpu = request.form['cpu']
        memory = request.form['memory']
        disk = request.form['disk']
        wanip = request.form['wanip']
        broadband_type = request.form['broadband_type']
        lanip = request.form['lanip']
        os = request.form['os']
        os_version = request.form['os_version']
        kvm_host = request.form['kvm_host']
        kvm_cpu_bind = request.form['kvm_cpu_bind']
        kvm_vnc_ip = request.form['kvm_vnc_ip']
        kvm_vnc_port = request.form['kvm_vnc_port']
        location = request.form['location']
        group = request.form['group']
        remark = request.form['remark']

        server = DBCmdbKVMVirtualServer.query.filter_by(hostname=origin_hostname).first()
        server.hostname = hostname
        server.cpu = cpu
        server.memory = memory
        server.disk = disk
        server.wanip = wanip
        server.wanip_alternate = ip_str2Int(wanip)
        server.lanip = lanip
        server.broadband_type = broadband_type
        server.os = os
        server.os_version = os_version
        server.kvm_host = kvm_host
        server.kvm_cpu_bind = kvm_cpu_bind
        server.kvm_vnc_ip = kvm_vnc_ip
        server.kvm_vnc_port = kvm_vnc_port
        server.location = location
        server.group = group
        server.remark = remark
        db_cmdb.session.commit()
        return redirect(url_for("cmdb.cmdb_server_vps_list"))
    return 'You should never reach here'


@cmdb.route('/server/vps/detail', methods=['GET', 'POST'])
@login_required
@is_cmdb_admin
def cmdb_server_vps_detail():
    hostname = request.args.get('hostname')
    server = DBCmdbKVMVirtualServer.query.filter_by(hostname=hostname).first()
    return render_template('cmdb_server_vps_detail.html', server=server)


@cmdb.route('/server/vps/del', methods=['GET'])
@login_required
@is_cmdb_admin
def cmdb_server_vps_del():
    hostname = request.args.get('hostname')

    DBCmdbKVMVirtualServer.query.filter_by(hostname=hostname).delete()
    DBCmdbKvmUser.query.filter_by(kvm_vs_hostname=hostname).delete()
    DBCmdbKvmProject.query.filter_by(kvm_vs_hostname=hostname).delete()
    db_cmdb.session.commit()

    return redirect(url_for("cmdb.cmdb_server_vps_list"))
