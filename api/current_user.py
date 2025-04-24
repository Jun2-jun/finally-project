# api/current_user.py

from flask import Blueprint, request, jsonify, session
from models.user import get_user_by_id

# ✅ 기능별 Blueprint 정의
current_user_bp = Blueprint('current_user', __name__, url_prefix='/api')

@current_user_bp.route('/current-user', methods=['GET'])
def get_current_user():
    user_id = session.get('user_id')

    if not user_id:
        return jsonify({'status': 'fail', 'message': '로그인 상태가 아닙니다.'}), 401

    user = get_user_by_id(user_id)

    if not user:
        return jsonify({'status': 'fail', 'message': '사용자를 찾을 수 없습니다.'}), 404

    return jsonify({
        'status': 'success',
        'user': {
            'username': user['username'],
            'email': user['email'],
            'birthdate': user['birthdate'],
            'phone': user['phone'],
            'address': user['address'],
            'address_detail': user['address_detail']
        }
    }), 200
