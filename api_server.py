from flask import Flask, Blueprint, request, jsonify
from flask_mysqldb import MySQL
from flask_cors import CORS
from datetime import datetime
import os
from werkzeug.utils import secure_filename
import json

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



# 예: 업로드 폴더를 프로젝트 디렉토리 하위의 'static/uploads'로 지정
UPLOAD_FOLDER = os.path.join(os.getcwd(), 'static', 'uploads')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)  # 폴더가 없으면 자동 생성

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


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

# 예약 리스트 - 대시보드 표시용
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

#7. Q&A qna.html
# Q&A 작성 API
@api_bp.route('/qna', methods=['POST'])
def create_qna():
    title = request.form.get('title')
    comment = request.form.get('comment')

    if not title or not comment:
        return jsonify({'status': 'fail', 'message': '제목과 내용을 입력해주세요.'}), 400

    image_urls = []
    files = request.files.getlist("images")
    upload_folder = app.config['UPLOAD_FOLDER']

    for file in files:
        if file and file.filename != '':
            filename = secure_filename(file.filename)
            filepath = os.path.join(upload_folder, filename)
            file.save(filepath)
            image_urls.append('/' + filepath.replace('\\', '/'))

    image_urls_json = json.dumps(image_urls)

    cur = mysql.connection.cursor()
    cur.execute("""
        INSERT INTO qna (title, comment, image_urls, category, created_at)
        VALUES (%s, %s, %s, %s, NOW())
    """, (title, comment, image_urls_json, '일반'))
    mysql.connection.commit()
    cur.close()

    return jsonify({'status': 'success', 'message': 'Q&A가 등록되었습니다.'}), 201

# Q/A 삭제
@api_bp.route('/qna/<int:post_id>', methods=['DELETE'])
def delete_qna(post_id):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM qna WHERE id = %s", (post_id,))
    mysql.connection.commit()
    affected_rows = cur.rowcount
    cur.close()

    if affected_rows > 0:
        return jsonify({'status': 'success', 'message': f'{post_id}번 Q&A가 삭제되었습니다.'}), 200
    else:
        return jsonify({'status': 'fail', 'message': '해당 ID의 Q&A가 존재하지 않습니다.'}), 404



# 8. 공지사항 notice.html
notices = []
next_notice_id = 1

# 공지사항 전체 목록 조회
@api_bp.route('/notices', methods=['GET'])

def get_notices():
    cur = mysql.connection.cursor()
    cur.execute("SELECT id, title, comment, created_at, views, image_urls FROM notice ORDER BY created_at DESC")
    notice = cur.fetchall()
    cur.close()
    return jsonify(notice)

# 공지사항 상세 조회
@api_bp.route('/notices/<int:post_id>', methods=['GET'])
def get_notice_detail(post_id):
    from flask_mysqldb import MySQL
    from MySQLdb.cursors import DictCursor
    import json

    cur = mysql.connection.cursor(cursorclass=DictCursor)
    cur.execute("SELECT id, title, comment, created_at, views, image_urls FROM notice WHERE id = %s", (post_id,))
    row = cur.fetchone()
    cur.close()

    if not row:
        return jsonify({"error": "Notice not found"}), 404

    if row.get('images'):
        try:
            row['images'] = json.loads(row['images'])
        except Exception:
            row['images'] = []

    print("API 응답 데이터:", row)
    return jsonify(row)


# 공지사항 작성
@api_bp.route('/notices', methods=['POST'])
def create_notice():
    title = request.form.get('title')
    comment = request.form.get('comment')

    if not title or not comment:
        return jsonify({'status': 'fail', 'message': '제목과 내용을 입력해주세요.'}), 400

    image_urls = []
    files = request.files.getlist('images')
    upload_folder = app.config['UPLOAD_FOLDER']

    for file in files:
        if file and file.filename != '':
            filename = secure_filename(file.filename)
            filepath = os.path.join(upload_folder, filename)
            file.save(filepath)
            # 웹 URL 형식으로 저장
            image_urls.append('/' + filepath.replace('\\', '/'))

    # JSON 형태로 저장
    image_urls_json = json.dumps(image_urls)

    cur = mysql.connection.cursor()
    cur.execute("""
        INSERT INTO notice (title, comment, image_urls)
        VALUES (%s, %s, %s)
    """, (title, comment, image_urls_json))
    mysql.connection.commit()
    cur.close()

    return jsonify({'status': 'success', 'message': '공지사항이 등록되었습니다.'}), 201

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