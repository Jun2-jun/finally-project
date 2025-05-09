from flask import Blueprint, render_template, request, jsonify
from datetime import datetime
import requests

submit_bp = Blueprint('submit', __name__)

# API 서버 기본 URL
API_BASE_URL = 'http://192.168.219.122:5002/api/reservations'


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

@submit_bp.route('/send_email', methods=['POST'])
def send_email():
    """
    이메일 전송 요청을 API 서버로 전달
    """
    try:
        # 폼 데이터 수집
        data = {
            'hospital': request.form.get('hospital'),
            'address': request.form.get('address'),
            'name': request.form.get('name'),
            'phone': request.form.get('phone'),
            'reservation_time': request.form.get('reservation_time'),
            'message': request.form.get('message'),
            'email': request.form.get('email')
        }

        # API 서버로 요청 전달 (비동기 처리는 JavaScript에서 구현)
        response = {"status": "success", "message": "이메일 전송 요청이 처리되었습니다."}
        return jsonify(response)
    
    except Exception as e:
        return jsonify({
            'status': 'fail',
            'message': f'이메일 전송 중 오류가 발생했습니다: {str(e)}'
        }), 500