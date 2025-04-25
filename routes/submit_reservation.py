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
    reservation_time = request.form.get('reservation_time')

    # if reservation_time_str:
    #     reservation_time_str = reservation_time_str.replace('T', ' ')
    #     reservation_time = datetime.strptime(reservation_time_str, '%Y-%m-%d %H:%M')

    return render_template("submit_reservation.html",
                           hospital=hospital,
                           address=address,
                           name=name,
                           phone=phone,
                           reservation_time=reservation_time,
                           message=message,
                           email=email)
