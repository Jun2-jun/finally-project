import hashlib
from functools import wraps
from flask import session, jsonify, request
import mysql.connector
from config import Config

# 비밀번호 해싱 함수 (SHA-256)
def hash_password(password):
    return hashlib.sha256(password.encode('utf-8')).hexdigest()

# 비밀번호 검증 함수
def check_password(hashed_password, password):
    return hashed_password == hashlib.sha256(password.encode('utf-8')).hexdigest()

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

def get_db_connection():
    conn = mysql.connector.connect(
        host=Config.MYSQL_HOST,
        user=Config.MYSQL_USER,
        password=Config.MYSQL_PASSWORD,
        database=Config.MYSQL_DB
    )
    return conn

# 관리자 인증 데코레이터
def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'username' not in session:
            return jsonify({
                'status': 'fail',
                'message': '로그인이 필요합니다.'
            }), 401

        if session['username'] != 'admin':
            return jsonify({
                'status': 'fail',
                'message': '관리자 권한이 필요합니다.'
            }), 403

        return f(*args, **kwargs)
    return decorated_function
