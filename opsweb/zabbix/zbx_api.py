# -*- coding: utf-8 -*-
from opsweb.conf import ZBX_ADMIN_USER, ZBX_ADMIN_PSW, ZBX_URL
from datetime import datetime, timedelta
import time
import json
import requests
from opsweb import app
from flask_login import login_required


def get_zbx_token():
    headers = {"Content-Type": "application/json"}
    params = {"user": ZBX_ADMIN_USER, "password": ZBX_ADMIN_PSW}
    data = {"jsonrpc": "2.0", "method": "user.login", "params": params, "id": 9}
    try:
        token = requests.post(ZBX_URL, headers=headers, data=json.dumps(data)).json()['result']
        return token
    except requests.exceptions.RequestException as e:
        app.logger.exception('Get zabbix auth token error.')
    return None


def get_zbx_alerts_count():
    headers = {"Content-Type": "application/json"}
    zbx_token = get_zbx_token()
    if zbx_token is None:
        return None
    chat_data = []
    session = requests.Session()
    for i in range(0, 9):
        date = datetime.strftime(datetime.now() - timedelta(i), '%Y-%m-%d')
        start, end = get_num_day_ago_timestamp(i)
        params = {"time_from": start, "time_till": end, "countOutput": True}
        data = {"jsonrpc": "2.0", "method": "alert.get", "params": params, "auth": zbx_token, "id": 9}
        try:
            alert_count = session.post(ZBX_URL, headers=headers, data=json.dumps(data)).json()['result']
            chat_data.append({"period": date, "alert_count": int(alert_count)})
        except requests.exceptions.RequestException as e:
            app.logger.exception('Get zabbix alerts count error.')
    session.close()
    return chat_data


@app.route('/zbx/api/alerts_count', methods=['GET'])
@login_required
def zbx_api_alerts_count():
    chat_data = get_zbx_alerts_count()
    return json.dumps(chat_data)


def get_num_day_ago_timestamp(num_days_ago):
    now = time.time()
    if num_days_ago == 0:
        end_day = time.localtime(now + 86400)
    elif num_days_ago > 0:
        end_day = time.localtime(now - (num_days_ago - 1) * 86400)
    else:
        return None
    end = time.struct_time((end_day.tm_year, end_day.tm_mon, end_day.tm_mday, 0, 0, 0, 0, 0, 0))
    start_day = time.localtime(now - num_days_ago * 86400)
    start = time.struct_time((start_day.tm_year, start_day.tm_mon, start_day.tm_mday, 0, 0, 0, 0, 0, 0))
    print(start, end)
    print(time.mktime(start), time.mktime(end))
    return time.mktime(start), time.mktime(end)
