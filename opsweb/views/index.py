# -*- coding: utf-8 -*-
from flask import render_template
from . import views
from flask_login import login_required
from ..statistics.confluence_stat import get_confluence_access_top10


@views.route('/')
@login_required
def index():
    confluence_access = get_confluence_access_top10()
    return render_template('index.html', confluence_access=confluence_access)
