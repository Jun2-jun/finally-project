from flask import Flask, jsonify
from config import config
from extensions import mysql, mail, session, init_upload_folder
from flask_cors import CORS
import os
from api import register_blueprints  # ✅ 이것만 있으면 됨


def create_app(config_name='default'):
    app = Flask(__name__)
    app.config.from_object(config[config_name])

    CORS(app, resources={r"/api/*": {"origins": [
        "http://localhost:5000",
        "http://127.0.0.1:5000",
        "http://192.168.219.189:5000",
        "http://192.168.219.87:5000"
    ]}}, supports_credentials=True)

    mysql.init_app(app)
    mail.init_app(app)
    session.init_app(app)
    init_upload_folder(app)

    # ✅ 모든 API 라우트 등록
    register_blueprints(app)

    @app.route('/')
    def index():
        return jsonify({
            "message": "API server is running", 
            "status": "ok",
            "version": "1.0.0"
        })

    return app

if __name__ == '__main__':
    app = create_app('development')
    app.run(host='0.0.0.0', port=5002, debug=app.config['DEBUG'])
