from flask import Blueprint, render_template, request, jsonify
from datetime import datetime
import requests

submit_bp = Blueprint('submit', __name__)


@submit_bp.route('/submit_reservation', methods=['POST'])
def submit_reservation():
    # form으로부터 데이터 받기
    hospital = request.form.get('hospital')
    address = request.form.get('address')
    name = request.form.get('name')
    phone = request.form.get('phone')
    message = request.form.get('message')
    email = request.form.get('email')
    reservation_time_raw = request.form.get('reservation_time')

    # datetime-local에서 오는 포맷은 "YYYY-MM-DDTHH:MM"
    try:
        if reservation_time_raw:
            reservation_time_str = reservation_time_raw.replace('T', ' ')
            reservation_time = datetime.strptime(reservation_time_str, '%Y-%m-%d %H:%M')
            formatted_time = reservation_time.strftime('%Y-%m-%d %H:%M')
        else:
            formatted_time = "예약 시간이 입력되지 않았습니다."
    except Exception:
        formatted_time = "날짜 형식이 올바르지 않습니다. (예: 2025-04-25 15:00)"

    return render_template("submit_reservation.html",
                           hospital=hospital,
                           address=address,
                           name=name,
                           phone=phone,
                           reservation_time=formatted_time,
                           message=message,
                           email=email)

