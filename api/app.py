from flask import Flask, jsonify
from config import config
from utils.decrypt_util import encrypt_response
from extensions import mysql, mail, session, init_upload_folder
from flask_cors import CORS
import os
import socket  # ✅ 추가

from api import register_blueprints  # ✅ 이것만 있으면 됨

def get_local_ip():
    """현재 PC의 로컬 IP를 가져오는 함수"""
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # 구글 DNS에 더미 연결 시도 → 자신의 IP 알아냄
        s.connect(('8.8.8.8', 80))
        ip = s.getsockname()[0]
    except Exception:
        ip = '127.0.0.1'
    finally:
        s.close()
    return ip

def create_app(config_name='default'):
    app = Flask(__name__)
    app.config.from_object(config[config_name])

    current_ip = get_local_ip()  # ✅ 현재 IP 가져오기

    CORS(app,
          supports_credentials=True,
          resources={r"/api/*": {"origins": [
              "http://localhost:5000",
              "http://127.0.0.1:5000",
              "http://192.168.219.72:5000"  # ✅ 내 현재 IP 자동 추가
            ],
            "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
            "allow_headers": "*"  # 모든 헤더 허용
          }})

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
