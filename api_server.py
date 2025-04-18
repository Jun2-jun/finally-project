from flask import Flask, Blueprint, request, jsonify
from flask_mysqldb import MySQL
from flask_cors import CORS

# Flask 앱 초기화
app = Flask(__name__)

# MySQL 설정 (하드코딩)
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'yourpassword'  # 비밀번호 없음
app.config['MYSQL_DB'] = 'hospital_app'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'  # 결과를 딕셔너리 형태로 반환

# MySQL 인스턴스 생성
mysql = MySQL(app)

# API Blueprint 생성
api_bp = Blueprint('api', __name__, url_prefix='/api')
CORS(api_bp)  # CORS 설정

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

    cur.execute("SELECT COUNT(*) FROM reservations WHERE DATE(schedule_date) = CURDATE()")
    today_sessions = cur.fetchone()[0]

    cur.execute("SELECT COUNT(*) FROM reservations WHERE schedule_date >= NOW() - INTERVAL 1 DAY")
    new_bookings = cur.fetchone()[0]

    cur.close()
    return jsonify({
        'users': users_count,
        'reservations': reservations_count,
        'new_bookings': new_bookings,
        'today_sessions': today_sessions
    })

# 7. 예약 리스트 - 대시보드 표시용
@api_bp.route('/upcoming-reservations', methods=['GET'])
def upcoming_reservations():
    cur = mysql.connection.cursor()
    cur.execute("""
        SELECT id, name, hospital, schedule_date
        FROM reservations
        ORDER BY schedule_date ASC
        LIMIT 5
    """)
    rows = cur.fetchall()
    cur.close()

    results = [
        {
            'id': row[0],
            'session_title': row[1],  # 예약자명
            'doctor': row[2],         # 병원명
            'datetime': row[3].strftime('%Y-%m-%d %H:%M')
        }
        for row in rows
    ]

    return jsonify(results)

# 테스트 API
@api_bp.route('/test', methods=['GET'])
def get_test():
    name = request.args.get("name")
    age = request.args.get("age")
    res = {
        "name": name,
        "age": age
    }
    return jsonify(res)

# Blueprint 등록
app.register_blueprint(api_bp)

# 메인 라우트
@app.route('/')
def index():
    return jsonify({"message": "API 서버가 정상적으로 실행 중입니다."})

# 실행 코드
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002, debug=True)