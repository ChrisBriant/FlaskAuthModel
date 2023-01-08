from flask import Flask

from config import Config
from app.extensions import db
from app.extensions import csrf
from app.extensions import migrate
from app.extensions import login_manager
from app.models.account import Account

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Initialize Flask extensions here
    db.init_app(app)
    csrf.init_app(app)
    migrate.init_app(app,db)
    login_manager.init_app(app)

    #Login Manager Config
    login_manager.login_view = 'auth.index'
    @login_manager.user_loader
    def load_user(user_id):
        return Account.query.get(int(user_id))

    # Register blueprints here
    from app.main import bp as main_bp
    app.register_blueprint(main_bp)

    from app.posts import bp as posts_bp
    app.register_blueprint(posts_bp, url_prefix='/posts')

    from app.questions import bp as questions_bp
    app.register_blueprint(questions_bp, url_prefix='/questions')

    from app.auth import bp as auth_bp
    app.register_blueprint(auth_bp, url_prefix='/auth')

    from app.authed_content import bp as authed_content_bp
    app.register_blueprint(authed_content_bp, url_prefix='/authedcontent')

    @app.route('/test/')
    def test_page():
        return '<h1>Testing the Flask Application Factory Pattern</h1>'

    

    return app