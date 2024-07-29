from flask import Flask
from config import Config

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    from app.routes import main, website_analyzer, crunchbase
    app.register_blueprint(main.bp)
    app.register_blueprint(website_analyzer.bp)
    app.register_blueprint(crunchbase.bp)

    return app