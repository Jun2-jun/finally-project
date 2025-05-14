from flask import Flask, Blueprint, render_template, redirect, url_for, session, request, flash, jsonify, current_app, make_response
from modules.connection import mysql, init_db
from datetime import datetime
from flask_mail import Mail, Message
from routes.submit_reservation import submit_bp
import os
from werkzeug.utils import secure_filename
import requests
from flask_cors import CORS
from flask_session import Session
from redis import Redis
import uuid

app = Flask(__name__)
app.secret_key = 'yougayoung123'
init_db(app)



app.register_blueprint(submit_bp)   
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 최대 16MB 업로드 허용

# IP 주소 중앙 관리 (환경 변수에서 가져오거나 기본값 사용)
app.config['SERVER_IP'] = os.environ.get('SERVER_IP', 'http://yourIP:5002')

# 세션 Redis 설정 추가
app.config['SESSION_TYPE'] = 'redis'
app.config['SESSION_REDIS'] = Redis(host='localhost', port=6379)
app.config['SESSION_COOKIE_DOMAIN'] = app.config['SERVER_IP']  # IP 중앙 관리 사용
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'  # 또는 'None'
app.config['SESSION_COOKIE_SECURE'] = True    # 로컬이라면 False
Session(app)  # 세션 객체 초기화

# 모든 템플릿에 전역 변수로 IP 주소 제공하는 컨텍스트 프로세서 추가
@app.context_processor
def inject_server_ip():
    return {'SERVER_IP': app.config['SERVER_IP']}

@app.route('/')
def home():
    # 디버깅: 콘솔에 세션 내용 출력
    current_app.logger.info(f"세션 정보: {session}")
    print(request.cookies)
    if 'user_id' in session:
        current_app.logger.info("로그인된 사용자입니다. /api/dashboard로 이동합니다.")
        return redirect('/dashboard')
    else:
        current_app.logger.info("로그인되지 않은 사용자입니다. index.html 렌더링.")
        return render_template("Main/index.html")

@app.route('/login')
def login():
    return render_template("login.html", now=datetime.now())

@app.route('/register')
def register():
    return render_template("register.html", now=datetime.now())

@app.route('/dashboard')
def dashboard():
    return render_template("Main/dashboard.html", now=datetime.now())

@app.route('/find')
def find():
    # URL에서 keyword 파라미터 가져오기 (예: /find?keyword=치과)
    keyword = request.args.get('keyword', '')
    
    # 템플릿에 keyword 파라미터 전달
    return render_template("find/find.html", now=datetime.now(), keyword=keyword)

@app.route('/admin')
def admin():
    return render_template("admin.html", now=datetime.now())

@app.route('/change_password')
def chage_password():
    return render_template("change_password.html", now=datetime.now())

@app.route('/ai')
def ai_chatbot():
    return render_template('AI/chatbot.html', now=datetime.now())  # 챗봇 HTML 템플릿

@app.route('/qna/post/<int:post_id>')
def qna_post_detail(post_id):
    return render_template('qna/qna_detail.html', post_id=post_id, now=datetime.now())

@app.route('/qna/post/test')
def qna_test():
    return '라우트는 작동 중입니다.'

@app.route('/qna/')
def qna_list():
    return render_template('qna/qna.html', now=datetime.now())
    
@app.route('/qna/write')
def qna_write():
    return render_template('qna/qna_write.html')

@app.route('/doctor')
def doctor():
    return render_template('doctor.html')

@app.route('/notice/')
def notice():
    return render_template("notice/notice.html", now=datetime.now())
    
@app.route('/notice/post/<int:post_id>')
def notice_detail(post_id):
    return render_template("notice/notice_detail.html")

@app.route('/reserve', methods=['GET', 'POST'])
def reserve():
    csrf_token = str(uuid.uuid4())
    session['csrf_token'] = csrf_token

    if request.method == 'POST':
        hospital_name = request.form.get('hospital_name', '')
        hospital_address = request.form.get('hospital_address', '')
    else:
        hospital_name = ''
        hospital_address = ''

    response = make_response(render_template(
        "reserve.html",
        hospital_name=hospital_name,
        hospital_address=hospital_address,
        csrf_token=csrf_token
    ))
    # 브라우저 캐시 방지
    response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, post-check=0, pre-check=0, max-age=0'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '-1'
    return response

@app.route('/submit_reservation', methods=['POST'])
def submit_reservation():
    # CSRF 토큰 검증
    form_token = request.form.get('csrf_token')
    session_token = session.pop('csrf_token', None)  # 사용 후 제거 (1회성)

    if not form_token or form_token != session_token:
        flash("이미 예약이 제출되었거나 유효하지 않은 접근입니다.")
        return redirect(url_for('reserve'))

    # 예약 정보 추출
    hospital = request.form.get('hospital')
    address = request.form.get('address')
    name = request.form.get('name')
    phone = request.form.get('phone')
    message = request.form.get('message')
    email = request.form.get('email')

    # 예약 완료 후 예약 정보 페이지 보여줌 (이메일 전송은 아님)
    return render_template('submit_reservation.html',
                           hospital=hospital,
                           address=address,
                           name=name,
                           phone=phone,
                           message=message,
                           email=email)

# Flask-Mail 설정
app.config['MAIL_SERVER'] = 'smtp.gmail.com'  # 예시로 Gmail SMTP 서버 사용
app.config['MAIL_PORT'] = 587
app.config['MAIL_USERNAME'] = 'doctorfutures2.0.0@gmail.com'  # 보내는 이메일 주소
app.config['MAIL_PASSWORD'] = 'ohbu uulg lugu yxyl'  # 앱 비밀번호(2차인증)
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False
app.config['MAIL_DEFAULT_SENDER'] = 'doctorfutures2.0.0@gmail.com'  # 기본 보낸 사람

mail = Mail(app)

@app.route("/send_email", methods=["POST"])
def send_email():
    hospital = request.form["hospital"]
    address = request.form["address"]
    name = request.form["name"]
    phone = request.form["phone"]
    message = request.form["message"]
    email = request.form.get("email", None)

    if email:
        print('가능')
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

        try:
            mail.send(msg)
            print("이메일 전송 완료")
        except Exception as e:
            print("이메일 전송 실패:", e)

    else:
        print('불가능: 이메일 주소 없음.')

    return render_template("find.html")

from datetime import datetime

@app.route('/mypage', methods=['GET', 'POST'])
def mypage():
    if request.method == 'POST':
        session['email'] = request.form.get('email')
        session['birthdate'] = request.form.get('birthdate')
        session['phone'] = request.form.get('phone')
        session['address'] = request.form.get('address')
        session['detail_address'] = request.form.get('detail_address')
        return redirect(url_for('Main/mypage'))

    # 기본값 설정 + 날짜 형식 처리
    birthdate = session.get('birthdate', '2000-01-01')
    try:
        # 문자열 형식을 datetime으로 변환 후 다시 YYYY-MM-DD로
        birthdate = datetime.strptime(birthdate, '%a, %d %b %Y %H:%M:%S GMT').strftime('%Y-%m-%d')
    except Exception:
        # 이미 YYYY-MM-DD거나 변환 실패 시 기본값 유지
        if len(birthdate) != 10:
            birthdate = '2000-01-01'

    user_data = {
        'userid': 'my_id',
        'email': session.get('email', 'myemail@example.com'),
        'birthdate': birthdate,
        'phone': session.get('phone', '010-1234-5678'),
        'address': session.get('address', '서울특별시 중구 세종대로'),
        'detail_address': session.get('detail_address', '101동 1001호')
    }

    return render_template("Main/mypage.html", user=user_data, now=datetime.now())


# 챗봇 메시지 처리 엔드포인트
@app.route('/chat', methods=['POST'])
def chat():
    user_message = request.json.get('message')

    # 예시: HuggingFace API 연동
    response = requests.post(
        'https://api-inference.huggingface.co/models/YourUsername/YourModelName',
        headers={'Authorization': 'Bearer YOUR_HUGGINGFACE_API_KEY'},
        json={"inputs": user_message}
    )

    if response.status_code == 200:
        data = response.json()
        bot_reply = data[0]["generated_text"] if data else "답변을 받을 수 없습니다."
    else:
        bot_reply = "모델 응답 실패 😥"

    return jsonify({"reply": bot_reply})

@app.route("/ent")
def ent_page():
    hospitals = [
        {
            'name': '센트럴이비인후과',
            'status': '진료중',
            'detail': '서울 중구',
            'distance': 200,
            'address': '서울 중구 퇴계로 10',
            'rating': 4.5,
            'review_count': 20,
            'category': '이비인후과',
            'image': None,
        },
        {
            'name': '서울코이비인후과',
            'status': '진료중',
            'detail': '서울 강남구',
            'distance': 150,
            'address': '서울 강남구 논현로 123',
            'rating': 4.8,
            'review_count': 15,
            'category': '이비인후과',
            'image': None,
        },
        {
            'name': '미소이비인후과',
            'status': '진료중',
            'detail': '서울 마포구',
            'distance': 320,
            'address': '서울 마포구 월드컵로 20',
            'rating': 4.7,
            'review_count': 30,
            'category': '이비인후과',
            'image': None,
        },
        {
            'name': '참이비인후과',
            'status': '진료중',
            'detail': '서울 종로구',
            'distance': 410,
            'address': '서울 종로구 율곡로 55',
            'rating': 4.2,
            'review_count': 12,
            'category': '이비인후과',
            'image': None,
        },
        {
            'name': '더웰이비인후과',
            'status': '진료중',
            'detail': '서울 송파구',
            'distance': 500,
            'address': '서울 송파구 송이로 88',
            'rating': 4.9,
            'review_count': 40,
            'category': '이비인후과',
            'image': None,
        },
        {
            'name': '하늘이비인후과',
            'status': '진료중',
            'detail': '서울 영등포구',
            'distance': 270,
            'address': '서울 영등포구 선유로 30',
            'rating': 4.3,
            'review_count': 18,
            'category': '이비인후과',
            'image': None,
        },
        {
            'name': '연세이비인후과',
            'status': '진료중',
            'detail': '서울 서초구',
            'distance': 350,
            'address': '서울 서초구 강남대로 240',
            'rating': 4.6,
            'review_count': 25,
            'category': '이비인후과',
            'image': None,
        },
        {
            'name': '제일이비인후과',
            'status': '진료중',
            'detail': '서울 구로구',
            'distance': 610,
            'address': '서울 구로구 디지털로 300',
            'rating': 4.4,
            'review_count': 10,
            'category': '이비인후과',
            'image': None,
        },
    ]
    return render_template("find/ent.html", hospitals=hospitals)

@app.route('/faq')
def faq_page():
    return render_template('faq.html')

@app.route('/magazine')
def magazine_page():
    return render_template('magazine.html')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
