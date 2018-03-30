from flask import Blueprint

views = Blueprint('views', __name__)

from . import index