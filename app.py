from flask import Flask, Blueprint, render_template, redirect, url_for, session, request, flash, jsonify, current_app
from modules.connection import mysql, init_db
from routes.auth import auth_bp
from datetime import datetime
from routes.reserve import reserve_bp
from routes.api import api_bp
from flask_mail import Mail, Message
from routes.submit_reservation import submit_bp
import os
from werkzeug.utils import secure_filename
from routes.qna import qna_bp
from routes.notice import notice_bp
import requests
from flask_cors import CORS


app = Flask(__name__)
app.secret_key = 'yougayoung123'
init_db(app)

app.register_blueprint(auth_bp, url_prefix="/auth")
app.register_blueprint(reserve_bp, url_prefix="/api")
app.register_blueprint(api_bp)
app.register_blueprint(submit_bp)
app.register_blueprint(qna_bp, url_prefix='/api/qna')
app.register_blueprint(notice_bp, url_prefix='/api/notice')
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 최대 16MB 업로드 허용
app.config['SESSION_COOKIE_PATH'] = '/'

@app.route('/')
def home():
    # 디버깅: 콘솔에 세션 내용 출력
    current_app.logger.info(f"세션 정보: {session}")

    if 'user_id' in session:
        current_app.logger.info("✅ 로그인된 사용자입니다. /api/dashboard로 이동합니다.")
        return redirect('http://192.168.219.189:5002/api/dashboard')
    else:
        current_app.logger.info("🔒 로그인되지 않은 사용자입니다. index.html 렌더링.")
        return render_template("index.html")

@app.route('/login')
def login():
    return render_template("login.html", now=datetime.now())

@app.route('/register')
def register():
    return render_template("register.html", now=datetime.now())

@app.route('/dashboard')
def dashboard():
    return render_template("dashboard.html", now=datetime.now())

@app.route('/find')
def find():
    return render_template("find.html", now=datetime.now())

@app.route('/admin')
def admin():
    return render_template("admin.html", now=datetime.now())

@app.route('/change_password')
def chage_password():
    return render_template("change_password.html", now=datetime.now())

#@app.route('/notice')
#def notice():
#    return render_template("notice.html", now=datetime.now())

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

@app.route('/notice/')
def notice():
    return render_template("notice/notice.html", now=datetime.now())
    
@app.route('/notice/post/<int:post_id>')
def notice_detail(post_id):
    return render_template("notice/notice_detail.html")

@app.route('/reserve', methods=['GET', 'POST'])
def reserve():
    if request.method == 'POST':
        hospital_name = request.form.get('hospital_name', '')
        hospital_address = request.form.get('hospital_address', '')
        return render_template("reserve.html", hospital_name=hospital_name, hospital_address=hospital_address)
    else:
        return render_template("reserve.html", hospital_name='', hospital_address='')

@app.route('/submit_reservation', methods=['POST'])
def submit_reservation():
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
        return redirect(url_for('mypage'))

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

    return render_template("mypage.html", user=user_data, now=datetime.now())


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




if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

