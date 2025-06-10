from flask import Flask, request, render_template, redirect
import json

app = Flask(__name__)

# 로그인 체크 함수: 각 사이트별 JSON 파일 확인
def check_login(user_id, password, json_file):
    try:
        with open(json_file) as f:
            users = json.load(f)
        for u in users:
            if u['id'] == user_id and u['pw'] == password:
                return True
    except Exception as e:
        print(f"파일 오류 또는 파싱 오류: {e}")
    return False


@app.route('/site1', methods=['GET', 'POST'])
def site1():
    if request.method == 'POST':
        user_id = request.form['username']
        pw = request.form['password']
        result = check_login(user_id, pw, 'users_site1.json')
        print(f"[site1] {user_id}:{pw} -> {'성공' if result else '실패'}")
        if result:
            return redirect('https://example.com')
        else:
            return "Login Failed", 401
    return render_template('site1_login.html')


@app.route('/site2', methods=['GET', 'POST'])
def site2():
    if request.method == 'POST':
        user_id = request.form['username']
        pw = request.form['password']
        result = check_login(user_id, pw, 'users_site2.json')
        print(f"[site2] {user_id}:{pw} -> {'성공' if result else '실패'}")
        if result:
            return redirect('https://example.com')
        else:
            return "Login Failed", 401
    return render_template('site2_login.html')


@app.route('/site3', methods=['GET', 'POST'])
def site3():
    if request.method == 'POST':
        user_id = request.form['username']
        pw = request.form['password']
        result = check_login(user_id, pw, 'users_site3.json')
        print(f"[site3] {user_id}:{pw} -> {'성공' if result else '실패'}")
        if result:
            return redirect('https://example.com')
        else:
            return "Login Failed", 401
    return render_template('site3_login.html')


@app.route('/')
def index():
    return render_template('index.html')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
