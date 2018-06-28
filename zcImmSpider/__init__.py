from flask import Flask


def create_app(config_name='default'):
    app = Flask(__name__)
    app.config.from_object('config')
    from .svr import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app
