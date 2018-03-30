# -*- coding: utf-8 -*-
from flask import render_template, current_app, flash, redirect, request, url_for
from . import cmdb
from opsweb import db_cmdb
from flask_login import login_required, current_user
from ..auth.admin import is_cmdb_admin
from ..dao.db_cmdb_physical_server import DBCmdbPhysicalServer
from ..dao.db_cmdb_physical_server_project import DBCmdbPhysicalServerProject
from ..dao.db_cmdb_physics_server_user import DBCmdbPhysicsServerUser
import datetime
import dateutil.parser
from ..utils.validate_ip import validate_ip


@cmdb.route('/server/physical/list', methods=['GET'])
@login_required
def cmdb_server_physical_list():
    try:
        servers = DBCmdbPhysicalServer.query.filter_by().all()
    except Exception as e:
        current_app.logger.error('Error: {}'.format(e))
        flash(current_app.config['MYSQL_REQUEST_ERROR'], 'alert')
        return redirect(request.referrer)
    else:
        return render_template('cmdb_server_physical_list.html', servers=servers)


@cmdb.route('/server/physical/add', methods=['GET', 'POST'])
@login_required
@is_cmdb_admin
def cmdb_server_physical_add():
    if request.method == 'GET':
        return render_template('cmdb_server_physical_add.html')

    if request.method == 'POST':
        hostname = request.form.get('hostname')
        buy_time = request.form.get('buy_time')
        company = request.form.get('company')
        service_no = request.form.get('service_no')
        cpu = int(request.form.get('cpu')) if request.form.get('cpu') != '' else 0
        cpu_physical_num = int(request.form.get('cpu_physical_num')) if request.form.get('cpu_physical_num') != '' else 0
        cpu_details = request.form['cpu_details']
        memory = int(request.form.get('memory')) if request.form.get('memory') != '' else 0
        memory_physical_num = int(request.form.get('memory_physical_num')) if request.form.get('memory_physical_num') != '' else 0
        memory_details = request.form['memory_details']
        disk = int(request.form.get('disk')) if request.form.get('disk') != '' else 0
        disk_physical_num = int(request.form.get('disk_physical_num')) if request.form.get('disk_physical_num') != '' else 0
        disk_details = request.form['disk_details']
        raid_level = int(request.form.get('raid_level')) if request.form.get('raid_level') != '' else 0
        raid_details = request.form['raid_details']
        power_physical_num = int(request.form.get('power_physical_num')) if request.form.get('power_physical_num') != '' else 0
        power_details = request.form['power_details']
        nic_physical_num = int(request.form.get('nic_physical_num')) if request.form.get('nic_physical_num') != '' else 0
        nic_details = request.form['nic_details']
        idrac = request.form['idrac']
        wanip = request.form['wanip']
        wanip_alternate = request.form['wanip_alternate']
        broadband_type = request.form['broadband_type']
        lanip = request.form['lanip']
        manageip = request.form['manageip']
        os = request.form['os']
        os_version = request.form['os_version']
        location = request.form['location']
        group = request.form['group']
        remark = request.form['remark']
        """
            variable do secondary modification
        """
        buy_time = dateutil.parser.parse(buy_time)
        create_time = datetime.datetime.now()
        for ip in [wanip, wanip_alternate, lanip, manageip]:
            if ip != '' and validate_ip(ip) is False:
                current_app.logger.error('warning: {} format error.'.format(ip))
                flash('{} {}'.format(ip, current_app.config['IP_FORMAT_ERROR']), 'alert')
                return redirect(request.referrer)

        try:
            server = DBCmdbPhysicalServer(hostname, buy_time, create_time, company, service_no, cpu, cpu_physical_num,
                                          cpu_details, memory, memory_physical_num, memory_details,
                                          disk, disk_physical_num, disk_details, raid_level, raid_details,
                                          power_physical_num, power_details, nic_physical_num, nic_details, idrac, wanip,
                                          wanip_alternate, broadband_type, lanip, manageip, os, os_version, location, group,
                                          remark)
            db_cmdb.session.add(server)
            db_cmdb.session.commit()
        except Exception as e:
            current_app.logger.error('Error: {}'.format(e))
            flash(current_app.config['MYSQL_REQUEST_ERROR'], 'alert')
            return redirect(request.referrer)
        else:
            return redirect(url_for("cmdb.cmdb_server_physical_list"))
    return None


@cmdb.route('/server/physical/edit', methods=['GET', 'POST'])
@login_required
@is_cmdb_admin
def cmdb_server_physical_edit():
    if request.method == 'GET':
        hostname = request.args.get('hostname', '')
        try:
            server = DBCmdbPhysicalServer.query.filter_by(hostname=hostname).first()
        except Exception as e:
            current_app.logger.error('Error: {}'.format(e))
            flash(current_app.config['MYSQL_REQUEST_ERROR'], 'alert')
            return redirect(request.referrer)
        else:
            return render_template('cmdb_server_physical_edit.html', server=server)

    if request.method == 'POST':
        origin_hostname = request.form.get('origin_hostname')
        hostname = request.form.get('hostname')
        buy_time = request.form.get('buy_time')
        company = request.form.get('company')
        service_no = request.form.get('service_no')
        cpu = int(request.form.get('cpu')) if request.form.get('cpu') != '' else 0
        cpu_physical_num = int(request.form.get('cpu_physical_num')) if request.form.get('cpu_physical_num') != '' else 0
        cpu_details = request.form['cpu_details']
        memory = int(request.form.get('memory')) if request.form.get('memory') != '' else 0
        memory_physical_num = int(request.form.get('memory_physical_num')) if request.form.get('memory_physical_num') != '' else 0
        memory_details = request.form['memory_details']
        disk = int(request.form.get('disk')) if request.form.get('disk') != '' else 0
        disk_physical_num = int(request.form.get('disk_physical_num')) if request.form.get('disk_physical_num') != '' else 0
        disk_details = request.form['disk_details']
        raid_level = int(request.form.get('raid_level')) if request.form.get('raid_level') != '' else 0
        raid_details = request.form['raid_details']
        power_physical_num = int(request.form.get('power_physical_num')) if request.form.get('power_physical_num') != '' else 0
        power_details = request.form['power_details']
        nic_physical_num = int(request.form.get('nic_physical_num')) if request.form.get('nic_physical_num') != '' else 0
        nic_details = request.form['nic_details']
        idrac = request.form['idrac']
        wanip = request.form['wanip']
        wanip_alternate = request.form['wanip_alternate']
        broadband_type = request.form['broadband_type']
        lanip = request.form['lanip']
        manageip = request.form['manageip']
        os = request.form['os']
        os_version = request.form['os_version']
        location = request.form['location']
        group = request.form['group']
        remark = request.form['remark']

        buy_time = dateutil.parser.parse(buy_time)
        create_time = datetime.datetime.now()
        for ip in [wanip, wanip_alternate, lanip, manageip]:
            if ip != '' and validate_ip(ip) is False:
                current_app.logger.error('warning: {} format error.'.format(ip))
                flash('{} {}'.format(ip, current_app.config['IP_FORMAT_ERROR']), 'alert')
                return redirect(request.referrer)

        try:
            server = DBCmdbPhysicalServer.query.filter_by(hostname=origin_hostname).first()
            server.hostname = hostname
            server.buy_time = buy_time
            server.create_time = create_time
            server.company = company
            server.service_no = service_no
            server.cpu = cpu
            server.cpu_physical_num = cpu_physical_num
            server.cpu_details = cpu_details
            server.memory = memory
            server.memory_physical_num = memory_physical_num
            server.memory_details = memory_details
            server.disk = disk
            server.disk_physical_num = disk_physical_num
            server.disk_details = disk_details
            server.raid_level = raid_level
            server.raid_details = raid_details
            server.power_physical_num = power_physical_num
            server.power_details = power_details
            server.nic_physical_num = nic_physical_num
            server.nic_details = nic_details
            server.idrac = idrac
            server.wanip = wanip
            server.wanip_alternate = wanip_alternate
            server.broadband_type = broadband_type
            server.lanip = lanip
            server.manageip = manageip
            server.os = os
            server.os_version = os_version
            server.location = location
            server.group = group
            server.remark = remark

            db_cmdb.session.commit()
        except Exception as e:
            current_app.logger.error('Error: {}'.format(e))
            flash(current_app.config['MYSQL_REQUEST_ERROR'], 'alert')
            return redirect(request.referrer)
        else:
            return redirect(url_for("cmdb.cmdb_server_physical_list"))
    return None


@cmdb.route('/server/physical/detail', methods=['GET', 'POST'])
@login_required
def cmdb_server_physical_detail():
    hostname = request.args.get('hostname', '')
    try:
        server = DBCmdbPhysicalServer.query.filter_by(hostname=hostname).first()
    except Exception as e:
        current_app.logger.error('Error: {}'.format(e))
        flash(current_app.config['MYSQL_REQUEST_ERROR'], 'alert')
        return redirect(request.referrer)
    else:
        return render_template('cmdb_server_physical_detail.html', server=server)


@cmdb.route('/server/physical/del', methods=['GET'])
@login_required
@is_cmdb_admin
def cmdb_server_physical_del():
    hostname = request.args.get('hostname')
    try:
        DBCmdbPhysicalServer.query.filter_by(hostname=hostname).delete()
        DBCmdbPhysicsServerUser.query.filter_by(physical_server_hostname=hostname).delete()
        DBCmdbPhysicalServerProject.query.filter_by(physical_server_hostname=hostname).delete()
        db_cmdb.session.commit()
    except Exception as e:
        current_app.logger.error('Error: {}'.format(e))
        flash(current_app.config['MYSQL_REQUEST_ERROR'], 'alert')
        return redirect(request.referrer)
    else:
        return redirect(url_for("cmdb.cmdb_server_physical_list"))
