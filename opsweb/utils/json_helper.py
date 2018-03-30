# -*- coding:utf-8 -*-
import json


def sqlalchemry_ob_to_json(objects):
    # TODO: 异常处理
    for obj in objects:
        _dict = obj.__dict__
        print(_dict)
        if '_sa_instance_state' in _dict:
            del _dict['_sa_instance_state']
        if 'create_time' in _dict:
            _dict['create_time'] = _dict['create_time'].strftime('%Y-%m-%d %H:%M:%S')
        if 'buy_time' in _dict:
            del _dict['buy_time']
            # _dict['buy_time'] = _dict['buy_time'].strftime('%Y-%m-%d %H:%M:%S')
    return json.dumps([o.__dict__ for o in objects])


def ad_sqlalchemry_ob_to_json(objects):
    # TODO: 异常处理
    for obj in objects:
        _dict = obj.__dict__
        if '_sa_instance_state' in _dict:
            del _dict['_sa_instance_state']
        if '_sa_instance_state' in _dict:
            del _dict['_sa_instance_state']
        if 'create_time' in _dict:
            _dict['create_time'] = _dict['create_time'].strftime('%Y-%m-%d %H:%M:%S')
    return json.dumps([o.__dict__ for o in objects])
