from flask import render_template, request, url_for, redirect
from app.authed_content import bp
from flask_login import login_required, current_user


@bp.route('/')
@login_required
def index():
    return render_template('authed_content/index.html', name=current_user.username)