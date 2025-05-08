from flask import Blueprint, jsonify
from utils.auth import login_required  # 기존 데코레이터 import

# /api/users prefix로 분리된 Blueprint
check_login_bp = Blueprint('check_login', __name__, url_prefix='/api/users')

#로그인 체크용 엔드포인트
@check_login_bp.route('/check-login', methods=['GET'])
@login_required
def check_login_status():
    return jsonify({'status': 'success', 'message': '로그인 상태입니다.'}), 200
