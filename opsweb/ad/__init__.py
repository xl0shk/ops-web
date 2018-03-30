from flask import Blueprint

ad = Blueprint('ad', __name__)

from . import ad_group, ad_user