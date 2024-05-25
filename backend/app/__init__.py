from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from config import Config

db = SQLAlchemy()
jwt = JWTManager()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    db.init_app(app)
    jwt.init_app(app)
    CORS(app)  # Allow CORS for all routes

    with app.app_context():
        from . import auth, meme, interactions, admin
        app.register_blueprint(auth.bp)
        app.register_blueprint(meme.bp)
        app.register_blueprint(interactions.bp)
        app.register_blueprint(admin.bp)
        db.create_all()

    return app
