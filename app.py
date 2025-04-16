from flask import Flask, render_template, request, redirect, flash
from flask_mail import Mail, Message
from modules.db import init_db
from routes.auth import auth_bp
from routes.reservation import reserve_bp

app = Flask(__name__)
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
app.config['MAIL_PASSWORD'] = '-'  # 이메일 계정 비밀번호
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_DEFAULT_SENDER'] = 'yougayoung114a@gmail.com'  # 기본 보낸 사람
app.secret_key = '`-`'

mail = Mail(app)

@app.route("/send_email", methods=["POST"])
def send_email():
    hospital = request.form["hospital"]
    address = request.form["address"]
    name = request.form["name"]
    phone = request.form["phone"]
    message = request.form["message"]
    
    # 이메일은 선택 사항이므로 get()을 사용하여 값이 없으면 None으로 처리
    email = request.form.get("email", None)  # 이메일 입력이 없을 경우 기본값 None

    # 이메일이 없으면 이메일 전송을 생략할 수 있음
    if email:
        # 이메일 내용 작성
        subject = f"병원 예약 확인 - {hospital}"
        body = f"""
        예약 정보:
        병원: {hospital}
        주소: {address}
        이름: {name}
        연락처: {phone}
        요청 사항: {message}
        이메일: {email}
        """
        
        # 이메일 전송
        msg = Message(subject=subject, recipients=[email])  # 예약한 사람에게 이메일 전송
        msg.body = body
        
        try:
            mail.send(msg)
            flash('예약이 완료되었습니다. 이메일이 전송되었습니다!', 'success')  # 성공 알림
        except Exception as e:
            flash(f'이메일 전송 중 오류가 발생했습니다: {e}', 'danger')  # 오류 알림
    else:
        flash('이메일이 입력되지 않았습니다.', 'warning')  # 이메일 입력 없을 때 경고

    return render_template("find.html")  # 이메일 전송 후 홈으로 리디렉션

if __name__ == '__main__':
    app.run(debug=True)
