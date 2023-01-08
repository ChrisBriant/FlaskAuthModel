from flask import Blueprint

bp = Blueprint('authed_content', __name__)

from app.authed_content import routes