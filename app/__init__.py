from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_migrate import Migrate
from flask_cors import CORS
from app.config import Config

db = SQLAlchemy()
ma = Marshmallow()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    CORS(app)
    db.init_app(app)
    ma.init_app(app)
    Migrate(app, db)

    # Register blueprints (API routes)
    from app.controllers import api_bp
    app.register_blueprint(api_bp, url_prefix="/api/v1")

    return app
