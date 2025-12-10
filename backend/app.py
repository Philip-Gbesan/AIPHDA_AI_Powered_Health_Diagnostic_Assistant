import os
from flask import Flask, send_from_directory
from backend.routes.predict import predict_bp
from backend.routes.feedback import feedback_bp
from backend.routes.admin import admin_bp
from flask_cors import CORS

def create_app():
    app = Flask(__name__, static_folder=None)
    CORS(app)

    @app.route('/')
    def index():
        return send_from_directory('frontend', 'index.html')

    @app.route('/<path:path>')
    def serve_static(path):
        return send_from_directory('frontend', path)

    app.register_blueprint(predict_bp, url_prefix="/api")
    app.register_blueprint(feedback_bp, url_prefix="/api")
    app.register_blueprint(admin_bp, url_prefix="/api/admin")

    return app

app = create_app()

if __name__ == "__main__":
    app.run(debug=True, use_reloader=False)
