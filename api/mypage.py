# api/mypage.py

from flask import Blueprint, render_template, session, redirect, url_for
from models.user import get_user_by_id

# ✅ URL prefix 명시적으로 부여
mypage_bp = Blueprint('mypage', __name__, url_prefix='/mypage')

@mypage_bp.route('/', methods=['GET'])
def mypage():
    user_id = session.get('user_id')
    if not user_id:
        return redirect(url_for('users.api_login'))  # 또는 정확한 라우트 네임

    user = get_user_by_id(user_id)
    return render_template('mypage.html', user=user)
