# -*- coding:utf-8 -*-
from flask import flash, redirect, url_for, request, current_app
from flask_login import current_user
from functools import wraps


def is_cmdb_admin(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        if current_user.cmdb_admin == 1:
            return func(*args, **kwargs)
        else:
            flash(current_app.config.get('WEB_ALERT', 'IS_NOT_CMDB_ADMIN'), 'alert')
            return redirect(request.referrer)

    return decorated_function


def is_zeus_admin(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        if current_user.zeus_admin == 1:
            return func(*args, **kwargs)
        else:
            flash(current_app.config.get('WEB_ALERT', 'IS_NOT_ZEUS_ADMIN'), 'alert')
            return redirect(request.referrer)

    return decorated_function


def is_ad_admin(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        if current_user.ad_admin == 1:
            return func(*args, **kwargs)
        else:
            flash(current_app.config.get('WEB_ALERT', 'IS_NOT_AD_ADMIN'), 'alert')
            return redirect(request.referrer)

    return decorated_function
