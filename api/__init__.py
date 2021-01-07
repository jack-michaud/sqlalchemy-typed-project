from flask import Flask


def make_app():
    app = Flask(__name__)
    app.config.from_object("api.config.Configuration")
    return app


def register_routes():
    from api import routes


def register_models():
    from api.models import user 
    user.User()


app = make_app()
register_routes()

register_models()
