# -*- coding: utf-8 -*-
from opsweb import db_cmdb


class DBCmdbKVMVirtualServer(db_cmdb.Model):
    __bind_key__ = 'cmdb'
    __tablename__ = 'kvm_virtual_server'
    id = db_cmdb.Column(db_cmdb.Integer, primary_key=True, autoincrement=True)
    hostname = db_cmdb.Column(db_cmdb.String(255), index=True)
    create_time = db_cmdb.Column(db_cmdb.DateTime)
    cpu = db_cmdb.Column(db_cmdb.Integer)
    memory = db_cmdb.Column(db_cmdb.Integer)
    disk = db_cmdb.Column(db_cmdb.Integer)
    wanip = db_cmdb.Column(db_cmdb.String(255))
    wanip_alternate = db_cmdb.Column(db_cmdb.String(255))
    broadband_type = db_cmdb.Column(db_cmdb.String(255))
    lanip = db_cmdb.Column(db_cmdb.String(255))
    os = db_cmdb.Column(db_cmdb.String(255))
    os_version = db_cmdb.Column(db_cmdb.String(255))
    kvm_host = db_cmdb.Column(db_cmdb.String(255))
    kvm_cpu_bind = db_cmdb.Column(db_cmdb.String(255))
    kvm_vnc_ip = db_cmdb.Column(db_cmdb.String(255))
    kvm_vnc_port = db_cmdb.Column(db_cmdb.Integer)
    location = db_cmdb.Column(db_cmdb.String(255))
    group = db_cmdb.Column(db_cmdb.String(255))
    remark = db_cmdb.Column(db_cmdb.String(255))

    def __init__(self, hostname, create_time, cpu, memory, disk, wanip, wanip_alternate, broadband_type, lanip, os,
                 os_version, kvm_host, kvm_cpu_bind, kvm_vnc_ip, kvm_vnc_port, location, group, remark):
        self.hostname = hostname
        self.create_time = create_time
        self.cpu = cpu
        self.memory = memory
        self.disk = disk
        self.wanip = wanip
        self.wanip_alternate = wanip_alternate
        self.broadband_type = broadband_type
        self.lanip = lanip
        self.os = os
        self.os_version = os_version
        self.kvm_host = kvm_host
        self.kvm_cpu_bind = kvm_cpu_bind
        self.kvm_vnc_ip = kvm_vnc_ip
        self.kvm_vnc_port = kvm_vnc_port
        self.location = location
        self.group = group
        self.remark = remark
