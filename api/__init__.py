from flask import Blueprint
from flask_cors import CORS

# API Blueprint 생성
api_bp = Blueprint('api', __name__, url_prefix='/api')

# 🔥 CORS 설정: 세션 쿠키 허용을 위해 정확한 origin + credentials 허용
CORS(api_bp, resources={r"/*": {"origins": "http://192.168.219.189:5000"}}, supports_credentials=True)

# 모든 모듈 임포트
from . import users, reservations, dashboard, qna, notices, ai_endpoints, current_user
