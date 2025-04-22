from flask import request, jsonify, session
from . import api_bp
from models.user import get_all_users, create_user, verify_user
from utils.auth import login_required, admin_required

# 1. 사용자 목록 - admin 페이지용
@api_bp.route('/users', methods=['GET'])
@admin_required
def get_users():
    try:
        users = get_all_users()
        return jsonify({
            'status': 'success',
            'data': users
        })
    except Exception as e:
        return jsonify({
            'status': 'fail',
            'message': f'사용자 목록 조회 중 오류가 발생했습니다: {str(e)}'
        }), 500

# 2. 회원가입 처리 API - register.html용
@api_bp.route('/register', methods=['POST'])
def api_register():
    try:
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')
        email = data.get('email')
        birthdate = data.get('birthdate')
        phone = data.get('phone')
        address = data.get('address')

        # 필수 필드 검증
        if not all([username, password, email]):
            return jsonify({
                'status': 'fail',
                'message': '아이디, 비밀번호, 이메일은 필수 입력 항목입니다.'
            }), 400

        # 사용자 등록
        user_id, error = create_user(username, password, email, birthdate, phone, address)
        
        if error:
            return jsonify({
                'status': 'fail',
                'message': error
            }), 400

        return jsonify({
            'status': 'success', 
            'message': '회원가입이 완료되었습니다.',
            'data': {
                'user_id': user_id,
                'username': username
            }
        }), 201
    except Exception as e:
        return jsonify({
            'status': 'fail',
            'message': f'회원가입 중 오류가 발생했습니다: {str(e)}'
        }), 500

# 3. 로그인 처리
@api_bp.route('/login', methods=['POST'])
def api_login():
    try:
        data = request.get_json() or {}
        username = data.get('username')
        password = data.get('password')
        
        if not username or not password:
            return jsonify({
                'status': 'fail',
                'message': '아이디와 비밀번호를 입력하세요.'
            }), 400

        # 사용자 인증
        user_data, error = verify_user(username, password)
        
        if error:
            return jsonify({
                'status': 'fail',
                'message': error
            }), 401

        # 세션에 사용자 정보 저장
        session['user_id'] = user_data.get('id')
        session['username'] = user_data.get('username')
        
        return jsonify({
            'status': 'success',
            'message': '로그인 성공',
            'data': user_data
        }), 200
    except Exception as e:
        return jsonify({
            'status': 'fail',
            'message': f'로그인 중 오류가 발생했습니다: {str(e)}'
        }), 500

# 4. 로그아웃 처리
@api_bp.route('/logout', methods=['POST'])
def api_logout():
    try:
        # 세션에서 사용자 정보 제거
        session.pop('user_id', None)
        session.pop('username', None)
        
        return jsonify({
            'status': 'success',
            'message': '로그아웃 성공'
        }), 200
    except Exception as e:
        return jsonify({
            'status': 'fail',
            'message': f'로그아웃 중 오류가 발생했습니다: {str(e)}'
        }), 500