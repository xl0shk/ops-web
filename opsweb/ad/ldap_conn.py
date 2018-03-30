# -*- coding: utf-8 -*-
from flask import current_app
from ldap3 import Server, Connection, ALL


class LDAPConn(object):
    def __init__(self):
        self._host = current_app.config['LDAP_SERVER']
        self._user = current_app.config['LDAP_ADM_USER']
        self._password = current_app.config['LDAP_ADM_PSW']
        self.ldap_server = Server(self._host, use_ssl=True, get_info=ALL)

    def ldap_conn(self):
        try:
            conn = Connection(self.ldap_server, self._user, self._password)
        except Exception as e:
            current_app.logger.exception('crowd connection error: '.format(e))
            return None
        else:
            return conn
