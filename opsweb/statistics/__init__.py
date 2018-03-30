from flask import Blueprint

statistics = Blueprint('statistics', __name__)

from . import confluence_stat
