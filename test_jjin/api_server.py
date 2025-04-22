from flask import Flask, Blueprint, request, jsonify, session
from flask_mysqldb import MySQL
from flask_cors import CORS
from datetime import datetime
import os
from werkzeug.utils import secure_filename
import json
from flask_mail import Mail, Message
from flask_session import Session
from redis import Redis
import bcrypt
import requests

# Flask 앱 초기화
app = Flask(__name__)

app.config.update({
    'SESSION_TYPE': 'redis',
    'SESSION_REDIS': Redis(host='localhost', port=6379),
    'SECRET_KEY': os.environ.get('SECRET_KEY', 'default_secret_key'),
    'SESSION_COOKIE_HTTPONLY': True,
    'SESSION_COOKIE_SECURE': True,
})
Session(app)

# MySQL 설정
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'doctor123!'
app.config['MYSQL_DB'] = 'doctor_future'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

# MySQL 인스턴스 생성
mysql = MySQL(app)

# API Blueprint 생성
api_bp = Blueprint('api', __name__, url_prefix='/api')
CORS(api_bp, resources={r"/*": {"origins": "*"}})  # 모든 도메인에서 접근 허용 (개발용)

# 업로드 폴더 설정
UPLOAD_FOLDER = os.path.join(os.getcwd(), 'static', 'uploads')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)  # 폴더가 없으면 자동 생성
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Flask-Mail 설정
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USERNAME'] = 'doctorfutures2.0.0@gmail.com'
app.config['MAIL_PASSWORD'] = 'hjnb eozw rnwt zijo'
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False
app.config['MAIL_DEFAULT_SENDER'] = 'doctorfutures2.0.0@gmail.com'

# Mail 인스턴스 생성
mail = Mail(app)

# 비밀번호 해싱 함수
def hash_password(password):
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

# 비밀번호 검증 함수
def check_password(hashed_password, password):
    return bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8'))

# 날짜 형식 변환 함수
def format_datetime(dt):
    if isinstance(dt, datetime):
        return dt.strftime('%Y-%m-%d %H:%M:%S')
    return dt

# 1. 사용자 목록 - admin 페이지용
@api_bp.route('/users', methods=['GET'])
def get_users():
    try:
        cur = mysql.connection.cursor()
        cur.execute("SELECT id, username, email FROM users")
        users = cur.fetchall()
        cur.close()
        return jsonify({
            'status': 'success',
            'data': users
        })
    except Exception as e:
        return jsonify({
            'status': 'fail',
            'message': f'사용자 목록 조회 중 오류가 발생했습니다: {str(e)}'
        }), 500

# 2. 예약 목록 - admin 페이지용
@api_bp.route('/reservations', methods=['GET'])
def get_reservations():
    try:
        cur = mysql.connection.cursor()
        cur.execute("SELECT id, name, phone, hospital, address, message, email, created_at FROM reservations")
        reservations = cur.fetchall()
        cur.close()
        
        # 날짜 형식 변환
        for res in reservations:
            res['created_at'] = format_datetime(res.get('created_at'))
            
        return jsonify({
            'status': 'success',
            'data': reservations
        })
    except Exception as e:
        return jsonify({
            'status': 'fail',
            'message': f'예약 목록 조회 중 오류가 발생했습니다: {str(e)}'
        }), 500

# 3. 병원 예약 생성 - reserve, submit_reserve.html POST용
@api_bp.route('/reservations', methods=['POST'])
def create_reservation():
    data = request.get_json()
    name = data.get('name')
    phone = data.get('phone')
    hospital = data.get('hospital')
    address = data.get('address')
    message = data.get('message', '')
    email = data.get('email', '')

    # 필수 필드 검증
    if not all([name, phone, hospital, address]):
        return jsonify({
            'status': 'fail',
            'message': '필수 정보가 누락되었습니다.'
        }), 400

    try:
        cur = mysql.connection.cursor()
        cur.execute("""
            INSERT INTO reservations (name, phone, hospital, address, message, email, created_at)
            VALUES (%s, %s, %s, %s, %s, %s, NOW())
        """, (name, phone, hospital, address, message, email))
        mysql.connection.commit()
        reservation_id = cur.lastrowid  # 새로 생성된 예약의 ID
        cur.close()
        
        # 이메일 발송 처리
        email_sent = False
        if email:
            try:
                subject = f"병원 예약 확인 - {hospital}"
                body = f"""
                안녕하세요, {name}님!

                아래와 같이 병원 예약이 완료되었습니다:

                ▷ 병원: {hospital}
                ▷ 주소: {address}
                ▷ 이름: {name}
                ▷ 연락처: {phone}
                ▷ 요청 사항: {message or "없음"}

                감사합니다!
                """

                msg = Message(subject=subject, recipients=[email])
                msg.body = body
                mail.send(msg)
                email_sent = True
            except Exception as e:
                print(f"이메일 전송 실패: {str(e)}")
        
        return jsonify({
            'status': 'success', 
            'message': '예약이 완료되었습니다.',
            'data': {
                'reservation_id': reservation_id
            },
            'email_sent': email_sent
        }), 201
    except Exception as e:
        return jsonify({
            'status': 'fail',
            'message': f'예약 생성 중 오류가 발생했습니다: {str(e)}'
        }), 500

# 4. 회원가입 처리 API - register.html용
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

        # 사용자 이름 중복 확인
        cur = mysql.connection.cursor()
        cur.execute("SELECT id FROM users WHERE username = %s", (username,))
        existing_user = cur.fetchone()
        if existing_user:
            cur.close()
            return jsonify({
                'status': 'fail',
                'message': '이미 사용 중인 아이디입니다.'
            }), 400

        # 비밀번호 해싱
        hashed_password = hash_password(password)

        # 사용자 등록
        cur.execute("""
            INSERT INTO users (username, password, email, birthdate, phone, address, created_at)
            VALUES (%s, %s, %s, %s, %s, %s, NOW())
        """, (username, hashed_password, email, birthdate, phone, address))
        mysql.connection.commit()
        user_id = cur.lastrowid
        cur.close()

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

# 5. 로그인 처리
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

        cur = mysql.connection.cursor()
        cur.execute("SELECT id, username, password, email, birthdate, phone, address FROM users WHERE username = %s", (username,))
        user = cur.fetchone()
        cur.close()
        
        if not user:
            return jsonify({
                'status': 'fail',
                'message': '아이디 또는 비밀번호가 올바르지 않습니다.'
            }), 401

        # 비밀번호 검증 (해싱된 비밀번호와 비교)
        stored_password = user.get('password')
        # 개발 편의를 위해 기존 평문 비밀번호도 허용 (실제 운영에서는 제거 필요)
        if not (check_password(stored_password, password) or stored_password == password):
            return jsonify({
                'status': 'fail',
                'message': '아이디 또는 비밀번호가 올바르지 않습니다.'
            }), 401

        # 세션에 사용자 정보 저장
        session['user_id'] = user.get('id')
        session['username'] = user.get('username')
        
        # 응답에 사용자 정보 포함 (비밀번호 제외)
        user_data = {
            'id': user.get('id'),
            'username': user.get('username'),
            'email': user.get('email'),
            'birthdate': format_datetime(user.get('birthdate')) if user.get('birthdate') else None,
            'phone': user.get('phone'),
            'address': user.get('address')
        }
        
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

# 6. 대시보드 요약 정보 - dashboard.html용
@api_bp.route('/dashboard-info', methods=['GET'])
def dashboard_info():
    try:
        cur = mysql.connection.cursor()
        cur.execute("SELECT COUNT(*) as count FROM users")
        users_count = cur.fetchone()['count']

        cur.execute("SELECT COUNT(*) as count FROM reservations")
        reservations_count = cur.fetchone()['count']

        cur.execute("SELECT COUNT(*) as count FROM reservations WHERE DATE(created_at) = CURDATE()")
        today_sessions = cur.fetchone()['count']

        cur.execute("SELECT COUNT(*) as count FROM reservations WHERE created_at >= NOW() - INTERVAL 1 DAY")
        new_bookings = cur.fetchone()['count']

        cur.close()
        return jsonify({
            'status': 'success',
            'data': {
                'users': users_count,
                'reservations': reservations_count,
                'new_bookings': new_bookings,
                'today_sessions': today_sessions
            }
        })
    except Exception as e:
        return jsonify({
            'status': 'fail',
            'message': f'대시보드 정보 조회 중 오류가 발생했습니다: {str(e)}'
        }), 500

# 예약 리스트 - 대시보드 표시용
@api_bp.route('/upcoming-reservations', methods=['GET'])
def upcoming_reservations():
    try:
        cur = mysql.connection.cursor()
        cur.execute("""
            SELECT id, name, hospital, created_at
            FROM reservations
            ORDER BY created_at DESC
            LIMIT 5
        """)
        reservations = cur.fetchall()
        cur.close()
        
        # 날짜 형식 변환
        for reservation in reservations:
            reservation['created_at'] = format_datetime(reservation.get('created_at'))
        
        return jsonify({
            'status': 'success',
            'data': reservations
        })
    except Exception as e:
        return jsonify({
            'status': 'fail',
            'message': f'예약 목록 조회 중 오류가 발생했습니다: {str(e)}'
        }), 500

# 7. Q&A - qna.html
# Q&A 목록 조회
@api_bp.route('/qna', methods=['GET'])
def get_qna():
    try:
        page = int(request.args.get('page', 1))
        per_page = int(request.args.get('per_page', 10))
        offset = (page - 1) * per_page

        cur = mysql.connection.cursor()
        
        # 전체 게시글 수 조회
        cur.execute("SELECT COUNT(*) as count FROM qna")
        total_count = cur.fetchone()['count']
        
        # 페이지네이션 적용하여 조회
        cur.execute("""
            SELECT id, title, comment, image_urls, created_at 
            FROM qna 
            ORDER BY created_at DESC
            LIMIT %s OFFSET %s
        """, (per_page, offset))
        qna_list = cur.fetchall()
        cur.close()
        
        # 날짜 형식 변환 및 이미지 URL 처리
        for item in qna_list:
            item['created_at'] = format_datetime(item.get('created_at'))
            if item.get('image_urls'):
                try:
                    item['image_urls'] = json.loads(item.get('image_urls'))
                except:
                    item['image_urls'] = []
        
        return jsonify({
            'status': 'success',
            'data': {
                'items': qna_list,
                'total': total_count,
                'page': page,
                'per_page': per_page,
                'total_pages': (total_count + per_page - 1) // per_page
            }
        })
    except Exception as e:
        return jsonify({
            'status': 'fail',
            'message': f'Q&A 목록 조회 중 오류가 발생했습니다: {str(e)}'
        }), 500

# Q&A 상세 조회
@api_bp.route('/qna/<int:post_id>', methods=['GET'])
def get_qna_detail(post_id):
    try:
        cur = mysql.connection.cursor()
        cur.execute("SELECT id, title, comment, image_urls, created_at FROM qna WHERE id = %s", (post_id,))
        qna = cur.fetchone()
        cur.close()

        if not qna:
            return jsonify({
                'status': 'fail',
                'message': '게시글을 찾을 수 없습니다.'
            }), 404
        
        # 날짜 형식 변환
        qna['created_at'] = format_datetime(qna.get('created_at'))
        
        # 이미지 URL JSON 파싱
        if qna.get('image_urls'):
            try:
                qna['image_urls'] = json.loads(qna.get('image_urls'))
            except:
                qna['image_urls'] = []
        
        return jsonify({
            'status': 'success',
            'data': qna
        })
    except Exception as e:
        return jsonify({
            'status': 'fail',
            'message': f'Q&A 상세 조회 중 오류가 발생했습니다: {str(e)}'
        }), 500

# Q&A 작성 API - JSON 또는 폼 데이터 둘 다 지원
@api_bp.route('/qna', methods=['POST'])
def create_qna():
    try:
        # JSON 또는 폼 데이터 처리
        if request.is_json:
            data = request.get_json()
            title = data.get('title')
            comment = data.get('comment')
            category = data.get('category', '일반')
            image_urls = []  # JSON 요청에서는 이미지를 처리하지 않음
        else:
            title = request.form.get('title')
            comment = request.form.get('comment')
            category = request.form.get('category', '일반')
            
            # 이미지 파일 처리
            image_urls = []
            files = request.files.getlist("images")
            upload_folder = app.config['UPLOAD_FOLDER']

            for file in files:
                if file and file.filename != '':
                    filename = secure_filename(file.filename)
                    filepath = os.path.join(upload_folder, filename)
                    file.save(filepath)
                    image_urls.append('/' + filepath.replace('\\', '/'))

        if not title or not comment:
            return jsonify({
                'status': 'fail', 
                'message': '제목과 내용을 입력해주세요.'
            }), 400

        # 이미지 URL을 JSON으로 변환
        image_urls_json = json.dumps(image_urls)

        cur = mysql.connection.cursor()
        cur.execute("""
            INSERT INTO qna (title, comment, image_urls, category, created_at)
            VALUES (%s, %s, %s, %s, NOW())
        """, (title, comment, image_urls_json, category))
        mysql.connection.commit()
        post_id = cur.lastrowid
        cur.close()

        return jsonify({
            'status': 'success', 
            'message': 'Q&A가 등록되었습니다.',
            'data': {
                'post_id': post_id
            }
        }), 201
    except Exception as e:
        return jsonify({
            'status': 'fail',
            'message': f'Q&A 등록 중 오류가 발생했습니다: {str(e)}'
        }), 500

# Q/A 삭제
@api_bp.route('/qna/<int:post_id>', methods=['DELETE'])
def delete_qna(post_id):
    try:
        cur = mysql.connection.cursor()
        cur.execute("DELETE FROM qna WHERE id = %s", (post_id,))
        mysql.connection.commit()
        affected_rows = cur.rowcount
        cur.close()

        if affected_rows > 0:
            return jsonify({
                'status': 'success',
                'message': f'{post_id}번 Q&A가 삭제되었습니다.'
            }), 200
        else:
            return jsonify({
                'status': 'fail',
                'message': '해당 ID의 Q&A가 존재하지 않습니다.'
            }), 404
    except Exception as e:
        return jsonify({
            'status': 'fail',
            'message': f'Q&A 삭제 중 오류가 발생했습니다: {str(e)}'
        }), 500

# Q/A 삭제 (POST 대체 - 클라이언트에서 DELETE를 지원하지 않는 경우)
@api_bp.route('/qna/<int:post_id>/delete', methods=['POST'])
def delete_qna_post(post_id):
    return delete_qna(post_id)

# 8. 공지사항 notice.html
# 공지사항 전체 목록 조회
@api_bp.route('/notices', methods=['GET'])
def get_notices():
    try:
        page = int(request.args.get('page', 1))
        per_page = int(request.args.get('per_page', 10))
        offset = (page - 1) * per_page

        cur = mysql.connection.cursor()
        
        # 전체 공지사항 수 조회
        cur.execute("SELECT COUNT(*) as count FROM notice")
        total_count = cur.fetchone()['count']
        
        # 페이지네이션 적용하여 조회
        cur.execute("""
            SELECT id, title, comment, created_at, views, image_urls 
            FROM notice 
            ORDER BY created_at DESC
            LIMIT %s OFFSET %s
        """, (per_page, offset))
        notices = cur.fetchall()
        cur.close()
        
        # 날짜 형식 변환
        for item in notices:
            item['created_at'] = format_datetime(item.get('created_at'))
            # 이미지 URL 처리
            if item.get('image_urls'):
                try:
                    item['image_urls'] = json.loads(item.get('image_urls'))
                except:
                    item['image_urls'] = []
        
        return jsonify({
            'status': 'success',
            'data': {
                'items': notices,
                'total': total_count,
                'page': page,
                'per_page': per_page,
                'total_pages': (total_count + per_page - 1) // per_page
            }
        })
    except Exception as e:
        return jsonify({
            'status': 'fail',
            'message': f'공지사항 목록 조회 중 오류가 발생했습니다: {str(e)}'
        }), 500

# 공지사항 상세 조회
@api_bp.route('/notices/<int:post_id>', methods=['GET'])
def get_notice_detail(post_id):
    try:
        # 조회수 증가
        cur = mysql.connection.cursor()
        cur.execute("UPDATE notice SET views = views + 1 WHERE id = %s", (post_id,))
        mysql.connection.commit()
        
        # 상세 정보 조회
        cur.execute("SELECT id, title, comment, created_at, views, image_urls FROM notice WHERE id = %s", (post_id,))
        notice = cur.fetchone()
        cur.close()

        if not notice:
            return jsonify({
                'status': 'fail',
                'message': '공지사항을 찾을 수 없습니다.'
            }), 404

        # 날짜 형식 변환
        notice['created_at'] = format_datetime(notice.get('created_at'))
        
        # 이미지 URL JSON 파싱
        if notice.get('image_urls'):
            try:
                notice['image_urls'] = json.loads(notice.get('image_urls'))
            except:
                notice['image_urls'] = []

        return jsonify({
            'status': 'success',
            'data': notice
        })
    except Exception as e:
        return jsonify({
            'status': 'fail',
            'message': f'공지사항 상세 조회 중 오류가 발생했습니다: {str(e)}'
        }), 500

# 공지사항 작성 - JSON 또는 폼 데이터 둘 다 지원
@api_bp.route('/notices', methods=['POST'])
def create_notice():
    try:
        # JSON 또는 폼 데이터 처리
        if request.is_json:
            data = request.get_json()
            title = data.get('title')
            comment = data.get('comment')
            image_urls = []  # JSON 요청에서는 이미지를 처리하지 않음
        else:
            title = request.form.get('title')
            comment = request.form.get('comment')
            
            # 이미지 파일 처리
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

        if not title or not comment:
            return jsonify({
                'status': 'fail', 
                'message': '제목과 내용을 입력해주세요.'
            }), 400

        # JSON 형태로 저장
        image_urls_json = json.dumps(image_urls)

        cur = mysql.connection.cursor()
        cur.execute("""
            INSERT INTO notice (title, comment, image_urls, created_at, views)
            VALUES (%s, %s, %s, NOW(), 0)
        """, (title, comment, image_urls_json))
        mysql.connection.commit()
        new_id = cur.lastrowid
        cur.close()

        return jsonify({
            'status': 'success', 
            'message': '공지사항이 등록되었습니다.',
            'data': {
                'notice_id': new_id
            }
        }), 201
    except Exception as e:
        return jsonify({
            'status': 'fail',
            'message': f'공지사항 등록 중 오류가 발생했습니다: {str(e)}'
        }), 500

# 공지사항 삭제
@api_bp.route('/notices/<int:post_id>', methods=['DELETE'])
def delete_notice(post_id):
    try:
        cur = mysql.connection.cursor()
        cur.execute("DELETE FROM notice WHERE id = %s", (post_id,))
        mysql.connection.commit()
        affected_rows = cur.rowcount
        cur.close()

        if affected_rows > 0:
            return jsonify({
                'status': 'success',
                'message': f'{post_id}번 공지사항이 삭제되었습니다.'
            }), 200
        else:
            return jsonify({
                'status': 'fail',
                'message': '해당 ID의 공지사항이 존재하지 않습니다.'
            }), 404
    except Exception as e:
        return jsonify({
            'status': 'fail',
            'message': f'공지사항 삭제 중 오류가 발생했습니다: {str(e)}'
        }), 500

# 공지사항 삭제 (POST 대체 - 클라이언트에서 DELETE를 지원하지 않는 경우)
@api_bp.route('/notices/<int:post_id>/delete', methods=['POST'])
def delete_notice_post(post_id):
    return delete_notice(post_id)

# 이메일 발송 API
@api_bp.route('/send-email', methods=['POST'])
def send_email_api():
    try:
        data = request.get_json()
        hospital = data.get('hospital')
        address = data.get('address')
        name = data.get('name')
        phone = data.get('phone')
        message = data.get('message', '')
        email = data.get('email')

        if not email:
            return jsonify({
                'status': 'fail', 
                'message': '이메일 주소가 필요합니다.'
            }), 400

        subject = f"병원 예약 확인 - {hospital}"
        body = f"""
        안녕하세요, {name}님!

        아래와 같이 병원 예약이 완료되었습니다:

        ▷ 병원: {hospital}
        ▷ 주소: {address}
        ▷ 이름: {name}
        ▷ 연락처: {phone}
        ▷ 요청 사항: {message or "없음"}

        감사합니다!
        """

        msg = Message(subject=subject, recipients=[email])
        msg.body = body
        mail.send(msg)
        
        return jsonify({
            'status': 'success', 
            'message': '이메일이 성공적으로 전송되었습니다.'
        }), 200
    except Exception as e:
        return jsonify({
            'status': 'fail',
            'message': f'이메일 전송 실패: {str(e)}'
        }), 500
    
# ai 호출 함수 
def call_gemini_api(prompt, api_key):
    api_url = 'https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent'
    
    url = f"{api_url}?key={api_key}"
    
    headers = {
        'Content-Type': 'application/json'
    }
    
    data = {
        "contents": [{
            "parts": [{"text": prompt}]
        }]
    }
    
    try:
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        return {"error": str(e)}

# ai 엔드 포인트
@api_bp.route('/ai', methods=['POST'])
def gemini_api():
    try:
        data = request.get_json()
        prompt = data.get('prompt')
        api_key = data.get('api_key')  # 클라이언트에서 API 키 제공 또는 환경 변수에서 가져오기
        
        if not prompt:
            return jsonify({
                'status': 'fail',
                'message': '프롬프트가 필요합니다.'
            }), 400
            
        if not api_key:
            api_key = os.environ.get('GEMINI_API_KEY','AIzaSyBwGAZB1xCnAW4XcWhY9ZhksBAxXyF5kvA')  # 환경 변수에서 가져오기
            
        if not api_key:
            return jsonify({
                'status': 'fail',
                'message': 'API 키가 필요합니다.'
            }), 400
        
        # Gemini API 호출
        result = call_gemini_api(prompt, api_key)
        
        # 에러 처리
        if 'error' in result:
            return jsonify({
                'status': 'fail',
                'message': f'Gemini API 호출 중 오류가 발생했습니다: {result["error"]}'
            }), 500
        
        return jsonify({
            'status': 'success',
            'data': result
        })
    except Exception as e:
        return jsonify({
            'status': 'fail',
            'message': f'Gemini API 호출 중 오류가 발생했습니다: {str(e)}'
        }), 500


# API 경로 추가 (앱 API URL과 일치시킴)
@api_bp.route('/posts', methods=['GET'])
def get_posts():
    return get_qna()  # qna API와 동일한 기능

@api_bp.route('/posts', methods=['POST'])
def create_post():
    return create_qna()  # qna API와 동일한 기능

# Blueprint 등록
app.register_blueprint(api_bp)

# 메인 라우트
@app.route('/')
def index():
    return jsonify({
        "message": "API server is running", 
        "status": "ok",
        "version": "1.0.0"
    })

# 실행 코드
if __name__ == '__main__':
   app.run(host='0.0.0.0', port=5002, debug=True)