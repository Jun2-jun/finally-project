from flask import Blueprint, request, jsonify, session
from extensions import mysql
from datetime import datetime
from models.reservation import (
    get_all_reservations,
    create_reservation,
    get_upcoming_reservations,
    get_user_reservations
)
from utils.auth import admin_required
from utils.email import send_reservation_confirmation

# 기능별 Blueprint 정의
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
    print(" 예약 라우터 진입", flush=True)
    try:
        data = request.get_json(force=True)
        print("받은 데이터:", data, flush=True)
    except Exception as e:
        print("❌ JSON 파싱 실패:", str(e), flush=True)
        return jsonify({'status': 'fail', 'message': '요청 형식 오류 (JSON 아님)'}), 400
    
    name = data.get('name')
    phone = data.get('phone')
    hospital = data.get('hospital')
    address = data.get('address')
    message = data.get('message', '')
    email = data.get('email', '')
    reservation_time = data.get('reservation_time')
    
    # 세션에서 user_id를 가져옴 (로그인된 경우)
    user_id = session.get('user_id')
    print(f"세션에서 가져온 user_id: {user_id}", flush=True)
    
    # 로그 추가
    print(f"파싱된 데이터: 이름={name}, 전화번호={phone}, 병원={hospital}, 시간={reservation_time}", flush=True)
    
    if not all([name, phone, hospital, address, reservation_time]):
        missing = []
        if not name: missing.append('이름')
        if not phone: missing.append('전화번호')
        if not hospital: missing.append('병원')
        if not address: missing.append('주소')
        if not reservation_time: missing.append('예약시간')
        
        return jsonify({
            'status': 'fail',
            'message': f'필수 정보가 누락되었습니다: {", ".join(missing)}'
        }), 400
    
    try:
        # DB 연결 상태 확인
        if not mysql.connection or mysql.connection.closed:
            print("❌ DB 연결이 닫혀있습니다. 재연결 시도...", flush=True)
            # 여기서 DB 재연결 로직 구현 필요
        
        reservation_id = create_reservation(
            name=name,
            phone=phone,
            hospital=hospital,
            address=address,
            message=message,
            email=email,
            user_id=user_id,  # 세션에서 가져온 user_id 사용
            reservation_time=reservation_time
        )
        
        print(f"✅ 예약 생성 성공: ID={reservation_id}", flush=True)
        
        email_sent = False
        if email:
            email_sent = send_reservation_confirmation(
                email=email,
                name=name,
                hospital=hospital,
                address=address,
                phone=phone,
                message=message,
                reservation_time=reservation_time
            )
            
        return jsonify({
            'status': 'success',
            'message': '예약이 완료되었습니다.',
            'data': {'reservation_id': reservation_id},
            'email_sent': email_sent
        }), 201
        
    except Exception as e:
        print(f"❌ 예약 생성 실패: {str(e)}", flush=True)
        import traceback
        traceback.print_exc()  # 상세 에러 로그 출력
        
        return jsonify({
            'status': 'fail',
            'message': f'예약 생성 중 오류가 발생했습니다: {str(e)}'
        }), 500


# 3. 대시보드용 최근 예약 목록
@reservations_bp.route('/upcoming', methods=['GET'])
def upcoming_reservations_api():
    if request.method == 'OPTIONS':
        return '', 200

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
        reservation_time = data.get('reservation_time')  # 👈 optional

        if not email:
            return jsonify({
                'status': 'fail', 
                'message': '이메일 주소가 필요합니다.'
            }), 400

        email_sent = send_reservation_confirmation(
            email=email,
            name=name,
            hospital=hospital,
            address=address,
            phone=phone,
            message=message,
            reservation_time=reservation_time
        )

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
