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
    reservation_time = request.form.get('reservation_time')
    message = request.form.get('message')
    email = request.form.get('email')

    # if reservation_time_str:
    #     reservation_time_str = reservation_time_str.replace('T', ' ')
    #     reservation_time = datetime.strptime(reservation_time_str, '%Y-%m-%d %H:%M')
    
    reservation_time_str = reservation_time.strftime('%Y-%m-%d %H:%M') if reservation_time else "yyyy-mm-dd hh:mm 형식으로 입력해주세요."

    return render_template("submit_reservation.html",
                           hospital=hospital,
                           address=address,
                           name=name,
                           phone=phone,
                           reservation_time=reservation_time,
                           message=message,
                           email=email)
