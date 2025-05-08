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

        username = session['username']

        conn = None
        cursor = None

        try:
            conn = get_db_connection()
            cursor = conn.cursor()

            query = "SELECT admin FROM users WHERE username = %s"
            cursor.execute(query, (username,))
            result = cursor.fetchone()

            if not result:
                return jsonify({
                    'status': 'fail',
                    'message': '사용자가 존재하지 않습니다.'
                }), 404

            admin_value = result[0]

            if admin_value != 1:
                return jsonify({
                    'status': 'fail',
                    'message': '관리자 권한이 필요합니다.'
                }), 403

        except Exception as e:
            print(f"DB 오류: {e}")
            return jsonify({
                'status': 'fail',
                'message': '서버 오류가 발생했습니다.'
            }), 500

        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

        return f(*args, **kwargs)

    return decorated_function
