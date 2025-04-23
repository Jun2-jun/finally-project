from flask import request, jsonify
from . import api_bp
from models.reservation import get_all_reservations, create_reservation, get_upcoming_reservations
from utils.auth import admin_required
from utils.email import send_reservation_confirmation
from flask import session

# 1. 예약 목록 - admin 페이지용
@api_bp.route('/reservations', methods=['GET'])
@admin_required
def get_reservations():
    try:
        reservations = get_all_reservations()
        return jsonify({
            'status': 'success',
            'data': reservations
        })
    except Exception as e:
        return jsonify({
            'status': 'fail',
            'message': f'예약 목록 조회 중 오류가 발생했습니다: {str(e)}'
        }), 500

# 2. 병원 예약 생성 - reserve, submit_reserve.html POST용
@api_bp.route('/reservations', methods=['POST'])
def create_reservation_api():
    data = request.get_json()
    name = data.get('name')
    phone = data.get('phone')
    hospital = data.get('hospital')
    address = data.get('address')
    message = data.get('message', '')
    email = data.get('email', '')
    
    # 로그인한 경우 user_id 가져오기
    user_id = session.get('user_id')

    # 필수 필드 검증
    if not all([name, phone, hospital, address]):
        return jsonify({
            'status': 'fail',
            'message': '필수 정보가 누락되었습니다.'
        }), 400

    try:
        # 예약 생성 시 user_id 전달
        reservation_id = create_reservation(name, phone, hospital, address, message, email, user_id)
        
        # 이메일 발송 처리
        email_sent = False
        if email:
            email_sent = send_reservation_confirmation(email, name, hospital, address, phone, message)
        
        return jsonify({
            'status': 'success', 
            'message': '예약이 완료되었습니다.',
            'data': {
                'reservation_id': reservation_id
            },
            'email_sent': email_sent
        }), 201
    except Exception as e:
        return jsonify({
            'status': 'fail',
            'message': f'예약 생성 중 오류가 발생했습니다: {str(e)}'
        }), 500

# 3. 예약 리스트 - 대시보드 표시용
@api_bp.route('/upcoming-reservations', methods=['GET'])
def upcoming_reservations_api():
    try:
        reservations = get_upcoming_reservations(limit=5)
        return jsonify({
            'status': 'success',
            'data': reservations
        })
    except Exception as e:
        return jsonify({
            'status': 'fail',
            'message': f'예약 목록 조회 중 오류가 발생했습니다: {str(e)}'
        }), 500

# 4. 이메일 발송 API
@api_bp.route('/send-email', methods=['POST'])
def send_email_api():
    try:
        data = request.get_json()
        hospital = data.get('hospital')
        address = data.get('address')
        name = data.get('name')
        phone = data.get('phone')
        message = data.get('message', '')
        email = data.get('email')

        if not email:
            return jsonify({
                'status': 'fail', 
                'message': '이메일 주소가 필요합니다.'
            }), 400

        # 이메일 발송
        email_sent = send_reservation_confirmation(email, name, hospital, address, phone, message)
        
        if email_sent:
            return jsonify({
                'status': 'success', 
                'message': '이메일이 성공적으로 전송되었습니다.'
            }), 200
        else:
            return jsonify({
                'status': 'fail',
                'message': '이메일 전송에 실패했습니다.'
            }), 500
    except Exception as e:
        return jsonify({
            'status': 'fail',
            'message': f'이메일 전송 실패: {str(e)}'
        }), 500