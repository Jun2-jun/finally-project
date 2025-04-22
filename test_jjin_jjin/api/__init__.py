from flask import Blueprint
from flask_cors import CORS

# API Blueprint 생성
api_bp = Blueprint('api', __name__, url_prefix='/api')
CORS(api_bp, resources={r"/*": {"origins": "*"}})  # 모든 도메인에서 접근 허용 (개발용)

# 모든 모듈 임포트
from . import users
from . import reservations
from . import dashboard
from . import qna
from . import notices
from . import ai_endpoints