from flask import Flask, render_template, request, redirect, flash
from flask_mail import Mail, Message
from modules.db import init_db
from routes.auth import auth_bp
from routes.reservation import reserve_bp

app = Flask(__name__)
app.secret_key = 'yougayoung123'
init_db(app)

app.register_blueprint(auth_bp, url_prefix="/auth")
app.register_blueprint(reserve_bp, url_prefix="/api")

@app.route('/')
def home():
    return render_template("home.html")

@app.route('/login')
def login():
    return render_template("login.html")

@app.route('/register')
def register():
    return render_template("register.html")

@app.route('/reserve')
def reserve():
    return render_template("reserve.html")

@app.route('/admin')
def admin():
    return render_template("admin.html")

@app.route('/find')
def find():
    return render_template("find.html")

@app.route('/reservation', methods=['GET', 'POST'])
def reservation():
    if request.method == 'POST':
        hospital_name = request.form.get('hospital_name', '')
        hospital_address = request.form.get('hospital_address', '')
    else:  # 혹시 사용자가 직접 주소로 접근할 경우 대비
        hospital_name = ''
        hospital_address = ''
    return render_template('reservation.html', hospital_name=hospital_name, hospital_address=hospital_address)

from flask import request, render_template

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
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'yougayoung114a@gmail.com'  # 보내는 이메일 주소
app.config['MAIL_PASSWORD'] = 'ddqk qpcy oeyu wglp'  # 앱 비밀번호(2차인증)
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_DEFAULT_SENDER'] = 'yougayoung114a@gmail.com'  # 기본 보낸 사람


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
            flash('이메일이 성공적으로 전송되었습니다.', 'success')
        except Exception as e:
            flash(f'이메일 전송 실패: {e}', 'danger')
    else:
        print('불가능')
        flash('이메일 주소가 입력되지 않았습니다.', 'warning')

    return render_template("find.html")

if __name__ == '__main__':
    app.run(debug=True)
