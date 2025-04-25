# api/users.py

from flask import Blueprint, request, jsonify, session
from models.user import get_all_users, create_user, verify_user, delete_user, update_user_info, get_user_by_id, change_user_password
from utils.auth import login_required, admin_required
from flask_cors import cross_origin

# ✅ users 전용 Blueprint 생성
users_bp = Blueprint('users', __name__, url_prefix='/api/users')

# 1. 사용자 목록 (관리자용)
@users_bp.route('/', methods=['GET'])
@admin_required
def get_users():
    try:
        users = get_all_users()
        return jsonify({'status': 'success', 'data': users})
    except Exception as e:
        return jsonify({'status': 'fail', 'message': f'사용자 목록 조회 오류: {str(e)}'}), 500

# 2. 회원가입
@users_bp.route('/register', methods=['POST'])
def api_register():
    try:
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')
        email = data.get('email')
        birthdate = data.get('birthdate')
        phone = data.get('phone')
        address = data.get('address')
        address_detail = data.get('address_detail')

        if not all([username, password, email]):
            return jsonify({'status': 'fail', 'message': '아이디, 비밀번호, 이메일은 필수 입력 항목입니다.'}), 400

        user_id, error = create_user(username, password, email, birthdate, phone, address, address_detail)
        if error:
            return jsonify({'status': 'fail', 'message': error}), 400

        return jsonify({
            'status': 'success',
            'message': '회원가입 완료',
            'data': {'user_id': user_id, 'username': username}
        }), 201
    except Exception as e:
        return jsonify({'status': 'fail', 'message': f'회원가입 중 오류: {str(e)}'}), 500

@users_bp.route('/login', methods=['POST', 'OPTIONS'])
@cross_origin(origins=[
    "http://localhost:5000",
    "http://127.0.0.1:5000",
    "http://192.168.219.189:5000"
], supports_credentials=True)
def api_login():
    if request.method == 'OPTIONS':
        return '', 204

    try:
        data = request.get_json() or {}
        username = data.get('username', '').strip()
        password = data.get('password')

        if not username or not password:
            return jsonify({'status': 'fail', 'message': '아이디와 비밀번호를 입력하세요.'}), 400

        user_data, error = verify_user(username, password)

        if error:
            return jsonify({'status': 'fail', 'message': error}), 401

        session['user_id'] = user_data.get('id')
        session['username'] = user_data.get('username')

        # ✅ admin이면 /admin으로 리다이렉트 포함
        response = {
            'status': 'success',
            'message': '로그인 성공',
            'data': user_data,
            'session': session.sid
        }

        if username.lower() == 'admin':
            response['redirect'] = '/admin'

        return jsonify(response), 200

    except Exception as e:
        return jsonify({'status': 'fail', 'message': f'로그인 오류: {str(e)}'}), 500


# 4. 로그아웃
@users_bp.route('/logout', methods=['POST'])
def api_logout():
    try:
        session.pop('user_id', None)
        session.pop('username', None)
        return jsonify({'status': 'success', 'message': '로그아웃 성공'}), 200
    except Exception as e:
        return jsonify({'status': 'fail', 'message': f'로그아웃 오류: {str(e)}'}), 500

# 5. 회원 탈퇴 (DELETE & POST 지원)
@users_bp.route('/withdraw', methods=['DELETE', 'POST'])
def withdraw_account():
    try:
        user_id = session.get('user_id')
        if not user_id:
            return jsonify({'status': 'fail', 'message': '로그인이 필요합니다.'}), 401

        success = delete_user(user_id)
        if success:
            session.pop('user_id', None)
            session.pop('username', None)
            return jsonify({'status': 'success', 'message': '회원 탈퇴 완료'}), 200
        else:
            return jsonify({'status': 'fail', 'message': '회원 탈퇴 처리 중 오류 발생'}), 400
    except Exception as e:
        return jsonify({'status': 'fail', 'message': f'탈퇴 중 오류: {str(e)}'}), 500

# 6. 사용자 정보 수정
@users_bp.route('/update', methods=['POST'])
@login_required
def update_user_information():
    try:
        user_id = session.get('user_id')
        if not user_id:
            return jsonify({'status': 'fail', 'message': '로그인이 필요합니다.'}), 401
        
        data = request.get_json()
        email = data.get('email')
        birthdate = data.get('birthdate')
        phone = data.get('phone')
        address = data.get('address')
        address_detail = data.get('address_detail')
        
        # 이메일은 필수 항목으로 처리
        if not email:
            return jsonify({'status': 'fail', 'message': '이메일은 필수 입력 항목입니다.'}), 400
        
        success, error = update_user_info(user_id, email, birthdate, phone, address, address_detail)
        
        if not success:
            return jsonify({'status': 'fail', 'message': error}), 400
            
        # 업데이트된 사용자 정보 가져오기
        updated_user = get_user_by_id(user_id)
            
        return jsonify({
            'status': 'success',
            'message': '사용자 정보가 성공적으로 수정되었습니다.',
            'data': updated_user
        }), 200
    except Exception as e:
        return jsonify({'status': 'fail', 'message': f'정보 수정 중 오류: {str(e)}'}), 500
    
# 7. 비밀번호 변경
@users_bp.route('/change-password', methods=['POST'])
@login_required
def change_password():
    try:
        user_id = session.get('user_id')
        data = request.get_json()
        current_password = data.get('current_password')
        new_password = data.get('new_password')
        
        success, error = change_user_password(user_id, current_password, new_password)
        
        if not success:
            return jsonify({'status': 'fail', 'message': error}), 400
            
        return jsonify({
            'status': 'success',
            'message': '비밀번호가 변경되었습니다.'
        }), 200
    except Exception as e:
        return jsonify({'status': 'fail', 'message': str(e)}), 500
