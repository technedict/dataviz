from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

# Initialize the database and login manager (will set up later)
db = SQLAlchemy()
login_manager = LoginManager()

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


def create_app():
    app = Flask(__name__)
    
    # Load configurations from config.py
    app.config.from_object('app.config.Config')

    # Initialize plugins
    db.init_app(app)
    login_manager.init_app(app)
    
    # Register blueprints (routes)
    from app.routes.auth import auth_bp
    from app.routes.data_upload import upload_bp
    from app.routes.eda import eda_bp
    from app.routes.visualization import viz_bp
    from app.routes.reports import reports_bp
    
    app.register_blueprint(auth_bp)
    app.register_blueprint(upload_bp)
    app.register_blueprint(eda_bp)
    app.register_blueprint(viz_bp)
    app.register_blueprint(reports_bp)
    
    return app
