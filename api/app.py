from flask import Flask, jsonify
from config import config
from utils.decrypt_util import encrypt_response
from extensions import mysql, mail, session, init_upload_folder
from flask_cors import CORS
import os
import socket  # ✅ 추가

from api import register_blueprints  # ✅ 이것만 있으면 됨


def create_app(config_name='default'):
    app = Flask(__name__)
    app.config.from_object(config[config_name])

    CORS(app, resources={r"/*": {"origins": "*"}}, supports_credentials=True)
    # CORS 설정: 모든 도메인 허용 (개발 시에만 사용, 배포 시에는 특정 도메인으로 제한해야 함)

    mysql.init_app(app)
    mail.init_app(app)
    session.init_app(app)
    init_upload_folder(app)

    register_blueprints(app)

    # 응답 암호화 미들웨어 등록
    app.after_request(encrypt_response)

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
