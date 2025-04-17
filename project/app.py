from flask import Flask, render_template, redirect, url_for, session, request, flash
from modules.connection import mysql, init_db
from routes.auth import auth_bp
from datetime import datetime
from routes.reserve import reserve_bp
from routes.api import api_bp
from flask_mail import Mail, Message
from routes.submit_reservation import submit_bp

app = Flask(__name__)
app.secret_key = 'yougayoung123'
init_db(app)

app.register_blueprint(auth_bp, url_prefix="/auth")
app.register_blueprint(reserve_bp, url_prefix="/api")
app.register_blueprint(api_bp)
app.register_blueprint(submit_bp)



@app.route('/')
def home():
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

@app.route('/mypage')
def mypage():
    return render_template("mypage.html", now=datetime.now())

@app.route('/admin')
def admin():
    return render_template("admin.html", now=datetime.now())

@app.route('/qna')
def qna():
    return render_template("qna.html", now=datetime.now())

@app.route('/notice')
def notice():
    return render_template("notice.html", now=datetime.now())

@app.route('/reserve', methods=['GET', 'POST'])
def reserve():
    if request.method == 'POST':
        hospital_name = request.form.get('hospital_name', '')
        hospital_address = request.form.get('hospital_address', '')
        return render_template("reserve.html", hospital_name=hospital_name, hospital_address=hospital_address)
    else:
        return render_template("reserve.html", hospital_name='', hospital_address='')

app.route('/submit_reservation', methods=['POST'])
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

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

