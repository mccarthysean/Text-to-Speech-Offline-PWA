from flask import Flask

def create_app():
    """Main factory function for creating the Flask app."""
    app = Flask(__name__)

    from .routes import main
    app.register_blueprint(main)

    return app
