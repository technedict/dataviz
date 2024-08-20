from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
#from flask_mail import Mail
from config import Config

# Initialize the database and login manager (will set up later)
db = SQLAlchemy()
login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.login_message = 'Please log in'
#mail = Mail()
migrate = Migrate()



def create_app(config_class=Config):
    app = Flask(__name__)

    # Load configurations from config.py
    app.config.from_object(config_class)

    # Initialize plugins
    db.init_app(app)
    login_manager.init_app(app)
    migrate.init_app(app, db)
    #mail.init_app(app)
    
    # Register blueprints (routes)
    from app.home import bp as main_bp
    from app.auth import bp as auth_bp
    from app.upload import bp as upload_bp
    from app.data import bp as data_bp
    
    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(upload_bp)
    app.register_blueprint(data_bp)

    
    return app
