from flask import Flask, jsonify
from config import config
from extensions import mysql, mail, session, init_upload_folder
from api import api_bp
from flask_cors import CORS
import os

def create_app(config_name='default'):
    """
    애플리케이션 팩토리 함수
    """
    app = Flask(__name__)
    
    # 설정 로드
    app.config.from_object(config[config_name])
    # CORS 설정 추가
    CORS(app, resources={r"/api/*": {"origins": [
    "http://localhost:5000",
    "http://127.0.0.1:5000",
    "http://192.168.59.1:5000",
    "http://192.168.219.221:5000",
    "http://192.168.219.203:5000",
    "http://192.168.219.111:5001"

]}}, supports_credentials=True)
    
    # 확장 초기화
    mysql.init_app(app)
    mail.init_app(app)
    session.init_app(app)
    
    # 업로드 폴더 초기화
    init_upload_folder(app)
    
    # API Blueprint 등록
    app.register_blueprint(api_bp)
    
    # 메인 라우트
    @app.route('/')
    def index():
        return jsonify({
            "message": "API server is running", 
            "status": "ok",
            "version": "1.0.0"
        })
        
    return app

# 애플리케이션 실행
if __name__ == '__main__':
    app = create_app('development')
    app.run(host='0.0.0.0', port=5002, debug=app.config['DEBUG'])