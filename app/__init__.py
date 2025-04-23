from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_migrate import Migrate
from .database import db
from flask_jwt_extended import JWTManager
from .routes import auth_routes, email_routes


ma = Marshmallow()
migrate = Migrate()
jwt = JWTManager()


def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///capyba.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['JWT_SECRET_KEY'] = 'segredo-super-seguro'  # idealmente use variável de ambiente


    db.init_app(app)
    ma.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    jwt.init_app(app)

    from .routes import pessoa_routes, contato_routes
    app.register_blueprint(pessoa_routes.bp)
    app.register_blueprint(contato_routes.bp)
    app.register_blueprint(auth_routes.bp)
    app.register_blueprint(email_routes.email_bp)


    return app
