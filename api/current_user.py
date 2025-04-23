from flask import request, jsonify, session
from . import api_bp
from models.user import get_user_by_id

@api_bp.route('/current-user', methods=['GET'])  # ✔️ endpoint 경로도 명확하게!
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
            'email': user['email']
        }
    }), 200
