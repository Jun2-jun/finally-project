import bcrypt
from functools import wraps
from flask import session, jsonify, request

# 비밀번호 해싱 함수
def hash_password(password):
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

# 비밀번호 검증 함수
def check_password(hashed_password, password):
    return bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8'))

# 로그인 필요한 경로를 위한 데코레이터
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return jsonify({
                'status': 'fail',
                'message': '로그인이 필요합니다.'
            }), 401
        return f(*args, **kwargs)
    return decorated_function

# 관리자 인증 데코레이터
def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return jsonify({
                'status': 'fail',
                'message': '로그인이 필요합니다.'
            }), 401
        
        # 여기에 관리자 체크 로직 추가
        # 예: 사용자가 관리자 역할을 가지고 있는지 확인
        # 데이터베이스 쿼리를 통해 사용자 역할 확인 필요
        
        return f(*args, **kwargs)
    return decorated_function