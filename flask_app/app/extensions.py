from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()

from flask_wtf.csrf import CSRFProtect
csrf = CSRFProtect()

from flask_migrate import Migrate
migrate = Migrate()

from flask_login import LoginManager
login_manager = LoginManager()

