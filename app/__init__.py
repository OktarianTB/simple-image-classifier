from flask import Flask, redirect, url_for
from .config import Config
from .image_classifier import create_classifier

my_image_classifier = create_classifier()


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(Config)
    app.secret_key = Config.SECRET_KEY

    from app.routes import classifier
    app.register_blueprint(classifier)
    app.register_error_handler(404, page_not_found)

    return app


def page_not_found(e):
    return redirect(url_for("classifier.home"))
