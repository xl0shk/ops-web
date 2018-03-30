# -*- coding: utf-8 -*-
from flask import current_app
from flask_login import login_required
from . import statistics
import requests
import json


def get_confluence_access_top10():
    headers = {"Content-Type": "application/json"}
    data = {"query": {"wildcard": {"url.raw": "/pages/*"}}, "size": 0, "aggs": {"top10": {"terms": {"field": "url.raw"}}}}
    res = requests.post(current_app.config['ES_CONFLUENCE_URL'], headers=headers, data=json.dumps(data)).json()
    confluence_access = res['aggregations']['top10']['buckets']
    return confluence_access


@statistics.route('/confluence/access', methods=['GET'])
@login_required
def statistics_confluence_access():
    confluence_access = get_confluence_access_top10()
    return json.dumps(confluence_access)



