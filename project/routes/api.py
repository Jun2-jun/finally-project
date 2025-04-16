from flask import Blueprint, request, jsonify
from modules.connection import mysql
from flask_cors import CORS

api_bp = Blueprint('api', __name__, url_prefix='/api')
CORS(api_bp)

# 1. 사용자 목록 - admin 페이지용
@api_bp.route('/users', methods=['GET'])
def get_users():
    cur = mysql.connection.cursor()
    cur.execute("SELECT id, username, email FROM users")
    users = cur.fetchall()
    cur.close()
    return jsonify(users)

# 2. 예약 목록 - admin 페이지용
@api_bp.route('/reservations', methods=['GET'])
def get_reservations():
    cur = mysql.connection.cursor()
    cur.execute("SELECT id, name, phone, hospital, address, message, email FROM reservations")
    reservations = cur.fetchall()
    cur.close()
    return jsonify(reservations)

# 3. 병원 예약 생성 - reserve, submit_reserve.html POST용
@api_bp.route('/reserve', methods=['POST'])
def create_reservation():
    data = request.get_json()
    name = data.get('name')
    phone = data.get('phone')
    hospital = data.get('hospital')
    address = data.get('address')
    message = data.get('message', '')
    email = data.get('email', '')

    cur = mysql.connection.cursor()
    cur.execute("""
        INSERT INTO reservations (name, phone, hospital, address, message, email)
        VALUES (%s, %s, %s, %s, %s, %s)
    """, (name, phone, hospital, address, message, email))
    mysql.connection.commit()
    cur.close()
    return jsonify({'status': 'success', 'message': '예약이 완료되었습니다.'}), 201

# 4. 회원가입 처리 API - register.html용
@api_bp.route('/register', methods=['POST'])
def api_register():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    email = data.get('email')
    birthdate = data.get('birthdate')
    phone = data.get('phone')
    address = data.get('address')

    cur = mysql.connection.cursor()
    cur.execute("""
        INSERT INTO users (username, password, email, birthdate, phone, address)
        VALUES (%s, %s, %s, %s, %s, %s)
    """, (username, password, email, birthdate, phone, address))
    mysql.connection.commit()
    cur.close()
    return jsonify({'status': 'success', 'message': '회원가입 완료'}), 201

# 5. 로그인 처리 API - login.html용
@api_bp.route('/login', methods=['POST'])
def api_login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM users WHERE username=%s AND password=%s", (username, password))
    user = cur.fetchone()
    cur.close()

    if user:
        return jsonify({'status': 'success', 'user': username})
    else:
        return jsonify({'status': 'fail', 'message': '로그인 실패'}), 401

# 6. 대시보드 요약 정보 - dashboard.html용
@api_bp.route('/dashboard-info', methods=['GET'])
def dashboard_info():
    cur = mysql.connection.cursor()
    cur.execute("SELECT COUNT(*) FROM users")
    users_count = cur.fetchone()[0]

    cur.execute("SELECT COUNT(*) FROM reservations")
    reservations_count = cur.fetchone()[0]

    cur.close()
    return jsonify({
        'users': users_count,
        'reservations': reservations_count
    })

@api_bp.route('/test', methods=['GET'])
def get_test():
    name = request.args.get("name")
    age = request.args.get("age")
    res = {
        "name": name,
        "age":age
    }
    return jsonify(res)