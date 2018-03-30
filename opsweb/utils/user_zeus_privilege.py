# -*- coding:utf-8 -*-
from opsweb.dao.db_cmdb_project_user import DBCmdbProjectUser
from opsweb.dao.db_cmdb_user import DBCmdbUser
from flask_login import current_user


def has_project_privilege(email, project_id):
    cmdb_user = DBCmdbUser.query.filter_by(email=email).first()
    user_info = DBCmdbProjectUser.query.filter_by(cmdb_user_id=cmdb_user.id).all()
    project_ids = []
    for user_privilege in user_info:
        project_ids.append(user_privilege.project_id)
    if project_id not in project_ids and current_user.zeus_admin != 1:
        return False
    else:
        return True
