# -*- coding:utf-8 -*-
from flask import flash, redirect, url_for, request, current_app
from opsweb.dao.db_cmdb_user import *
from opsweb.dao.db_zeus_user_info import *
from flask_login import current_user
from functools import wraps


# from opsweb.conf import *

#
def check_ad_user_admin(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        ad_admins = DBCmdbUser.query.filter_by(ad_admin=1).all()
        for ad_admin in ad_admins:
            if current_user.name in ad_admin.name:
                return func(*args, **kwargs)
        flash(current_app.config.get('IS_NOT_AD_ADMIN'), 'alert')
        return redirect(url_for("ad_user_bp.ad_user_list"))

    return decorated_function


def check_ad_group_admin(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        ad_admins = DBCmdbUser.query.filter_by(ad_admin=1).all()
        for ad_admin in ad_admins:
            if current_user.name in ad_admin.name:
                return func(*args, **kwargs)
        flash(current_app.config.get('IS_NOT_AD_ADMIN'), 'alert')
        return redirect(url_for("ad_user_bp.ad_group_list"))

    return decorated_function


def check_zeus_admin(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        admin_privilege = DBCmdbUser.query.filter_by(email=current_user.email).first()
        if admin_privilege.zeus_admin == 1:
            return func(*args, **kwargs)
        flash(current_app.config.get('IS_NOT_AD_ADMIN'), 'alert')
        return redirect(request.referrer)

    return decorated_function
