from flask import Flask, request, render_template, redirect, session, url_for
import json

app = Flask(__name__)
app.secret_key = 'your-secret-key'  # 세션 사용을 위한 키

# 로그인 체크 함수
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

# 루트 페이지 (로그인 페이지 겸용)
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        user_id = request.form.get('username')
        pw = request.form.get('password')
        result = check_login(user_id, pw, 'users_site3.json')
        print(f"[site3] {user_id}:{pw} -> {'성공' if result else '실패'}")
        if result:
            session['user'] = user_id
            return redirect(url_for('main'))
        else:
            return "Login Failed", 401
    return render_template('site3_login.html')

# 로그인 성공 후 페이지
@app.route('/main')
def main():
    if 'user' in session:
        return render_template('main.html', username=session['user'])
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
