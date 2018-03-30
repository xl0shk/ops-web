# -*- coding: utf-8 -*-
from opsweb import db_cmdb


class DBCmdbPhysicalServer(db_cmdb.Model):
    __bind_key__ = 'cmdb'
    __tablename__ = 'physical_server'
    id = db_cmdb.Column(db_cmdb.Integer, primary_key=True, autoincrement=True)
    hostname = db_cmdb.Column(db_cmdb.String(255), index=True)
    buy_time = db_cmdb.Column(db_cmdb.DateTime)
    create_time = db_cmdb.Column(db_cmdb.DateTime)
    company = db_cmdb.Column(db_cmdb.String(255))
    service_no = db_cmdb.Column(db_cmdb.String(255))
    cpu = db_cmdb.Column(db_cmdb.Integer)
    cpu_physical_num = db_cmdb.Column(db_cmdb.Integer)
    cpu_details = db_cmdb.Column(db_cmdb.String(255))
    memory = db_cmdb.Column(db_cmdb.Integer)
    memory_physical_num = db_cmdb.Column(db_cmdb.Integer)
    memory_details = db_cmdb.Column(db_cmdb.String(255))
    disk = db_cmdb.Column(db_cmdb.Integer)
    disk_physical_num = db_cmdb.Column(db_cmdb.Integer)
    disk_details = db_cmdb.Column(db_cmdb.String(255))
    raid_level = db_cmdb.Column(db_cmdb.Integer)
    raid_details = db_cmdb.Column(db_cmdb.String(255))
    power_physical_num = db_cmdb.Column(db_cmdb.Integer)
    power_details = db_cmdb.Column(db_cmdb.String(255))
    nic_physical_num = db_cmdb.Column(db_cmdb.Integer)
    nic_details = db_cmdb.Column(db_cmdb.String(255))
    idrac = db_cmdb.Column(db_cmdb.String(255))
    wanip = db_cmdb.Column(db_cmdb.String(255))
    wanip_alternate = db_cmdb.Column(db_cmdb.String(255))
    broadband_type = db_cmdb.Column(db_cmdb.String(255))
    lanip = db_cmdb.Column(db_cmdb.String(255))
    manageip = db_cmdb.Column(db_cmdb.String(255))
    os = db_cmdb.Column(db_cmdb.String(255))
    os_version = db_cmdb.Column(db_cmdb.String(255))
    location = db_cmdb.Column(db_cmdb.String(255))
    group = db_cmdb.Column(db_cmdb.String(255))
    remark = db_cmdb.Column(db_cmdb.String(255))

    def __init__(self, hostname, buy_time, create_time, company, service_no, cpu, cpu_physical_num, cpu_details, memory,
                 memory_physical_num, memory_details, disk, disk_physical_num, disk_details, raid_level, raid_details,
                 power_physical_num, power_details, nic_physical_num, nic_details, idrac, wanip, wanip_alternate,
                 broadband_type, lanip, manageip, os, os_version, location, group, remark):
        self.hostname = hostname
        self.buy_time = buy_time
        self.create_time = create_time
        self.company = company
        self.service_no = service_no
        self.cpu = cpu
        self.cpu_physical_num = cpu_physical_num
        self.cpu_details = cpu_details
        self.memory = memory
        self.memory_physical_num = memory_physical_num
        self.memory_details = memory_details
        self.disk = disk
        self.disk_physical_num = disk_physical_num
        self.disk_details = disk_details
        self.raid_level = raid_level
        self.raid_details = raid_details
        self.power_physical_num = power_physical_num
        self.power_details = power_details
        self.nic_physical_num = nic_physical_num
        self.nic_details = nic_details
        self.idrac = idrac
        self.wanip = wanip
        self.wanip_alternate = wanip_alternate
        self.broadband_type = broadband_type
        self.lanip = lanip
        self.manageip = manageip
        self.os = os
        self.os_version = os_version
        self.location = location
        self.group = group
        self.remark = remark
