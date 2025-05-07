# api/__init__.py

from .users import users_bp
from .mypage import mypage_bp
from .reservations import reservations_bp
from .dashboard import dashboard_bp
from .qna import qna_bp
from .notices import notices_bp
from .ai_endpoints import ai_bp
from .current_user import current_user_bp
from .check_login import check_login_bp  # ✅ 추가
from .xor import patient_info_bp  # ✅ 추가

def register_blueprints(app):
    # 기능별 Blueprint 등록
    app.register_blueprint(users_bp)            # /api/users
    app.register_blueprint(mypage_bp)           # /mypage
    app.register_blueprint(reservations_bp)     # /api/reservations
    app.register_blueprint(dashboard_bp)        # /api/dashboard
    app.register_blueprint(qna_bp)              # /api/qna
    app.register_blueprint(notices_bp)          # /api/notices
    app.register_blueprint(ai_bp)               # /api/ai
    app.register_blueprint(current_user_bp)     # /api/current-user
    app.register_blueprint(check_login_bp)  # ✅ 이 줄 추가!
    app.register_blueprint(patient_info_bp)    # ✅ 이 줄 추가

# api/current_user.py
from flask import Blueprint, jsonify, session
from models.user import get_user_by_id

current_user_bp = Blueprint('current_user', __name__, url_prefix='/api')

@current_user_bp.route('/current-user', methods=['GET'])
def get_current_user():
    user_id = session.get('user_id')
    if not user_id:
        return jsonify({'status': 'fail', 'message': '로그인이 필요합니다.'}), 401

    user = get_user_by_id(user_id)
    if not user:
        return jsonify({'status': 'fail', 'message': '사용자를 찾을 수 없습니다.'}), 404

    return jsonify({
        'status': 'success',
        'user': user
    })
