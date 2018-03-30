# http api CMDB资产管理　权限列表
import json

# from opsweb.cmdb import cmdb_api
from . import cmdb_api
from opsweb.dao.db_cmdb_cloud_project import DBCmdbCloudProject
from opsweb.dao.db_cmdb_cloud_user import DBCmdbCloudUser
from opsweb.dao.db_cmdb_cloud_virtual_server import DBCmdbCloudVirtualServer
from opsweb.dao.db_cmdb_kvm_project import DBCmdbKvmProject
from opsweb.dao.db_cmdb_kvm_user import DBCmdbKvmUser
from opsweb.dao.db_cmdb_kvm_virtual_server import DBCmdbKVMVirtualServer
from opsweb.dao.db_cmdb_physical_server import DBCmdbPhysicalServer
from opsweb.dao.db_cmdb_physical_server_project import DBCmdbPhysicalServerProject
from opsweb.dao.db_cmdb_physics_server_user import DBCmdbPhysicsServerUser
from opsweb.dao.db_cmdb_project import DBCmdbProject
from opsweb.dao.db_cmdb_user import DBCmdbUser
from opsweb.utils.json_helper import sqlalchemry_ob_to_json


@cmdb_api.route('/server/physical', methods=['GET'])
def cmdb_server_physical_list_api():
    try:
        servers = DBCmdbPhysicalServer.query.filter_by().all()
    except Exception as e:
        return json.dumps({'error': 'encode json wrong'})
    return sqlalchemry_ob_to_json(servers)


@cmdb_api.route('/server/privilege', methods=['GET'])
def cmdb_server_privilege_list_api():
    try:
        servers = DBCmdbPhysicsServerUser.query.filter_by().all()
    except Exception as e:
        return json.dumps({'error': 'encode json wrong'})
    return sqlalchemry_ob_to_json(servers)


@cmdb_api.route('/server/project', methods=['GET'])
def cmdb_server_project_list_api():
    try:
        servers = DBCmdbPhysicalServerProject.query.filter_by().all()
    except Exception as e:
        return json.dumps({'error': 'encode json wrong'})
    return sqlalchemry_ob_to_json(servers)


@cmdb_api.route('/vps', methods=['GET'])
def cmdb_server_vps_list_api():
    try:
        servers = DBCmdbKVMVirtualServer.query.filter_by().all()
    except Exception as e:
        return json.dumps({'error': 'encode json wrong'})
    return sqlalchemry_ob_to_json(servers)


@cmdb_api.route('/kvm/privilege', methods=['GET'])
def cmdb_kvm_privilege_list_api():
    try:
        servers = DBCmdbKvmUser.query.filter_by().all()
    except Exception as e:
        return json.dumps({'error': 'encode json wrong'})
    return sqlalchemry_ob_to_json(servers)


@cmdb_api.route('/kvm/project', methods=['GET'])
def cmdb_kvm_project_list_api():
    try:
        servers = DBCmdbKvmProject.query.filter_by().all()
    except Exception as e:
        return json.dumps({'error': 'encode json wrong'})
    return sqlalchemry_ob_to_json(servers)


@cmdb_api.route('/cloud/privilege', methods=['GET'])
def cmdb_cloud_privilege_list_api():
    try:
        servers = DBCmdbCloudUser.query.filter_by().all()
    except Exception as e:
        return json.dumps({'error': 'encode json wrong'})
    return sqlalchemry_ob_to_json(servers)


@cmdb_api.route('/server/cloudvps', methods=['GET'])
def cmdb_server_cloudvps_list_api():
    try:
        servers = DBCmdbCloudVirtualServer.query.filter_by().all()
    except Exception as e:
        return json.dumps({'error': 'encode json wrong'})
    return sqlalchemry_ob_to_json(servers)


@cmdb_api.route('/cloud/project', methods=['GET'])
def cmdb_cloud_project_list_api():
    try:
        servers = DBCmdbCloudProject.query.filter_by().all()
    except Exception as e:
        return json.dumps({'error': 'encode json wrong'})
    return sqlalchemry_ob_to_json(servers)


@cmdb_api.route('/project', methods=['GET'])
def cmdb_api_project():
    try:
        projects = DBCmdbProject.query.filter_by().all()
    except Exception as e:
        return json.dumps({'error': 'encode json wrong'})
    return sqlalchemry_ob_to_json(projects)


@cmdb_api.route('/user', methods=['GET'])
def cmdb_user_list_api():
    try:
        cmdb_users = DBCmdbUser.query.all()
    except Exception as e:
        return json.dumps({'error': 'encode json wrong'})
    return sqlalchemry_ob_to_json(cmdb_users)
