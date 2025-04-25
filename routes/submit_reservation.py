from flask import Blueprint, render_template, request
from datetime import datetime

submit_bp = Blueprint('submit', __name__)

@submit_bp.route('/submit_reservation', methods=['POST'])
def submit_reservation():
    # form으로부터 데이터 받기
    hospital = request.form.get('hospital')
    address = request.form.get('address')
    name = request.form.get('name')
    phone = request.form.get('phone')
    date = request.form.get('date')      # 예: '2025-04-30'
    time = request.form.get('time')      # 예: '09:30'
    message = request.form.get('message')
    email = request.form.get('email')

    # 날짜와 시간 합치기
    reservation_str = f"{date} {time}"   # '2025-04-30 09:30'
    try:
        reservation_time = datetime.strptime(reservation_str, "%Y-%m-%d %H:%M")
    except ValueError:
        return "잘못된 날짜/시간 형식입니다.", 400

    return render_template("submit_reservation.html",
                           hospital=hospital,
                           address=address,
                           name=name,
                           phone=phone,
                           reservation_time=reservation_time,
                           message=message,
                           email=email)
