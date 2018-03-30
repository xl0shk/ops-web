from flask import Blueprint

cmdb = Blueprint('cmdb', __name__)
cmdb_api = Blueprint('cmdb_api', __name__)

from . import server_physical, server_vps, server_cloudvps, cmdb_user, project, server_privilege, cmdb_api
from . import kvm_privilege, cloud_privilege, server_project, kvm_project, cloud_project, user_project_privilege
