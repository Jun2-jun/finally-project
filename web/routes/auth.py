from flask import Blueprint, request, render_template
from modules.connection import mysql


auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['POST'])
def login_post():
    username = request.form.get('username')
    password = request.form.get('password')
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM users WHERE username=%s AND password=%s", (username, password))
    user = cur.fetchone()
    cur.close()
    if user:
        return f"로그인 성공! {username}님 환영합니다."
    else:
        return "로그인 실패, 다시 시도하세요."

@auth_bp.route('/register', methods=['POST'])
def register_post():
    username = request.form.get('username')
    password = request.form.get('password')
    cur = mysql.connection.cursor()
    cur.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (username, password))
    mysql.connection.commit()
    cur.close()
    return "회원가입 완료! <a href='/login'>로그인하기</a>"
