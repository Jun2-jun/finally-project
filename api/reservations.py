# api/reservations.py

from flask import Blueprint, request, jsonify, session
from models.reservation import (
    get_all_reservations,
    create_reservation,
    get_upcoming_reservations,
    get_user_reservations
)
from utils.auth import admin_required
from utils.email import send_reservation_confirmation

# ✅ 기능별 Blueprint 정의
reservations_bp = Blueprint('reservations', __name__, url_prefix='/api/reservations')

# 1. 관리자용 예약 전체 조회
@reservations_bp.route('/', methods=['GET'])
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

# 2. 예약 생성 (사용자 or 비회원)
@reservations_bp.route('/', methods=['POST'])
def create_reservation_api():
    print("받은 요청 데이터:", data)
    print("name:", name, "| phone:", phone, "| hospital:", hospital, "| address:", address)
    data = request.get_json()
    name = data.get('name')
    phone = data.get('phone')
    hospital = data.get('hospital')
    address = data.get('address')
    message = data.get('message', '')
    email = data.get('email', '')
    user_id = data.get('user_id')  # 로그인 유저일 경우

    if not all([name, phone, hospital, address]):
        return jsonify({
            'status': 'fail',
            'message': '필수 정보가 누락되었습니다.'
        }), 400

    try:
        reservation_id = create_reservation(name, phone, hospital, address, message, email, user_id)
        email_sent = False
        if email:
            email_sent = send_reservation_confirmation(email, name, hospital, address, phone, message)

        return jsonify({
            'status': 'success',
            'message': '예약이 완료되었습니다.',
            'data': {'reservation_id': reservation_id},
            'email_sent': email_sent
        }), 201
    except Exception as e:
        return jsonify({
            'status': 'fail',
            'message': f'예약 생성 중 오류가 발생했습니다: {str(e)}'
        }), 500

# 3. 대시보드용 최근 예약 목록
@reservations_bp.route('/upcoming', methods=['GET'])
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

# 4. 이메일 재발송
@reservations_bp.route('/send-email', methods=['POST'])
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

        email_sent = send_reservation_confirmation(email, name, hospital, address, phone, message)

        if email_sent:
            return jsonify({'status': 'success', 'message': '이메일 전송 성공'}), 200
        else:
            return jsonify({'status': 'fail', 'message': '이메일 전송 실패'}), 500
    except Exception as e:
        return jsonify({'status': 'fail', 'message': f'이메일 전송 오류: {str(e)}'}), 500

# 5. 사용자별 예약 목록 조회
@reservations_bp.route('/user/<int:user_id>', methods=['GET'])
def get_user_reservations_api(user_id):
    try:
        reservations = get_user_reservations(user_id)
        return jsonify({
            'status': 'success',
            'data': reservations
        })
    except Exception as e:
        return jsonify({
            'status': 'fail',
            'message': f'사용자 예약 조회 오류: {str(e)}'
        }), 500
