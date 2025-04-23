from flask import Flask, jsonify
from config import config
from extensions import mysql, mail, session, init_upload_folder
from api import api_bp
import os

def create_app(config_name='default'):
    """
    애플리케이션 팩토리 함수
    """
    app = Flask(__name__)
    
    # 설정 로드
    app.config.from_object(config[config_name])
    
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
    app = create_app(os.environ.get('FLASK_ENV', 'development'))
    app.run(host='0.0.0.0', port=5002, debug=app.config['DEBUG'])