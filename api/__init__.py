from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from .routes import init_routes

db = SQLAlchemy()

def create_app(vectorIndex):
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
    
    db.init_app(app)
    
    init_routes(app, vectorIndex)
    
    return app