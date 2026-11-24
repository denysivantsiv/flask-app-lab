from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from sqlalchemy.orm import DeclarativeBase
from app.config import config

class Base(DeclarativeBase):
    pass

db = SQLAlchemy(model_class=Base)
migrate = Migrate()

def create_app(config_name='default'):
    app = Flask(__name__)
    app.config.from_object(config[config_name])

    db.init_app(app)
    migrate.init_app(app, db)

    from app.posts import post_bp
    app.register_blueprint(post_bp)

    @app.route('/')
    @app.route('/home')
    def home():
        return render_template('base.html')

    @app.errorhandler(404)
    def not_found(e):
        return render_template('404.html'), 404

    return app