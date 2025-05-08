from flask import Blueprint, request, jsonify, session
from models.user import get_all_users, create_user, verify_user, delete_user, update_user_info, get_user_by_id, change_user_password
from utils.auth import login_required, admin_required
from flask_cors import cross_origin
from utils.auth import hash_password
from utils.auth import check_password
from utils.decrypt_util import decrypt_request_json
from flask_mail import Mail, Message
import random, string
from extensions import mail

#users 전용 Blueprint 생성
users_bp = Blueprint('users', __name__, url_prefix='/api/users')

# 1. 사용자 목록 (관리자용)
@users_bp.route('/', methods=['GET'])
@admin_required
def get_users():
    try:
        users = get_all_users()
        return jsonify({'status': 'success', 'data': users})
    except Exception as e:
        return jsonify({'status': 'fail', 'message': f'사용자 목록 조회 오류: {str(e)}'}), 500

# 2. 회원가입
@users_bp.route('/register', methods=['POST'])
def api_register():
    try:
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')
        email = data.get('email')
        birthdate = data.get('birthdate')
        phone = data.get('phone')
        address = data.get('address')
        address_detail = data.get('address_detail')

        if not all([username, password, email]):
            return jsonify({'status': 'fail', 'message': '아이디, 비밀번호, 이메일은 필수 입력 항목입니다.'}), 400

        user_id, error = create_user(username, password, email, birthdate, phone, address, address_detail)
        if error:
            return jsonify({'status': 'fail', 'message': error}), 400

        return jsonify({
            'status': 'success',
            'message': '회원가입 완료',
            'data': {'user_id': user_id, 'username': username}
        }), 201
    except Exception as e:
        return jsonify({'status': 'fail', 'message': f'회원가입 중 오류: {str(e)}'}), 500
#3. 로그인
@users_bp.route('/login', methods=['POST', 'OPTIONS'])
@cross_origin(origins=[
    "http://localhost:5000",
    "http://127.0.0.1:5000",
    "http://192.168.219.72:5000",
    "http://192.168.219.176:5000"
], supports_credentials=True)
def api_login():
    if request.method == 'OPTIONS':
        return '', 204

    try:
        data = request.get_json() or {}
        username = data.get('username', '').strip()
        password = data.get('password')

        if not username or not password:
            return jsonify({'status': 'fail', 'message': '아이디와 비밀번호를 입력하세요.'}), 400

        user_data, error = verify_user(username, password)

        if error:
            return jsonify({'status': 'fail', 'message': error}), 401

        session['user_id'] = user_data.get('id')
        session['username'] = user_data.get('username')
        session['admin'] = user_data.get('admin')

        response = {
            'status': 'success',
            'message': '로그인 성공',
            'data': user_data,
            'session': session.sid
        }

        if username.lower() == 'admin':
            response['redirect'] = '/admin'

        return jsonify(response), 200

    except Exception as e:
        return jsonify({'status': 'fail', 'message': f'로그인 오류: {str(e)}'}), 500


# 4. 로그아웃
@users_bp.route('/logout', methods=['POST'])
def api_logout():
    try:
        session.pop('user_id', None)
        session.pop('username', None)
        return jsonify({'status': 'success', 'message': '로그아웃 성공'}), 200
    except Exception as e:
        return jsonify({'status': 'fail', 'message': f'로그아웃 오류: {str(e)}'}), 500

# 5. 회원 탈퇴
@users_bp.route('/withdraw', methods=['POST', 'OPTIONS'])
@cross_origin(origins=["http://192.168.219.72:5000"], supports_credentials=True)
@login_required
def withdraw_account():
    if request.method == 'OPTIONS':
        return '', 204

    try:
        data = request.get_json(force=True)
        print("[DEBUG] 탈퇴 요청 데이터:", data)

        if not data or 'password' not in data:
            return jsonify({'success': False, 'message': "'password' 키가 없습니다.", 'debug': str(data)}), 400

        input_password = data['password']
        user_id = session.get('user_id')
        print("[DEBUG] 현재 user_id:", user_id)

        # 🔥 여기서 None 확인 추가!
        user = get_user_by_id(user_id)
        if not user:
            return jsonify({'success': False, 'message': '사용자 정보를 찾을 수 없습니다.'}), 404

        if not check_password(user['password'], input_password):
            return jsonify({'success': False, 'message': '비밀번호가 일치하지 않습니다.'}), 400

        success = delete_user(user_id)
        if success:
            session.pop('user_id', None)
            session.pop('username', None)
            return jsonify({'success': True, 'message': '회원 탈퇴 완료'}), 200
        else:
            return jsonify({'success': False, 'message': '회원 탈퇴 처리 중 오류 발생'}), 400

    except Exception as e:
        print("[ERROR] 탈퇴 중 예외 발생:", str(e))
        return jsonify({'success': False, 'message': f"탈퇴 중 오류: {str(e)}"}), 500

# 6. 사용자 정보 수정
@users_bp.route('/update', methods=['POST'])
@login_required
def update_user_information():
    try:
        user_id = session.get('user_id')
        if not user_id:
            return jsonify({'status': 'fail', 'message': '로그인이 필요합니다.'}), 401

        data = request.get_json()
        email = data.get('email')
        birthdate = data.get('birthdate')
        phone = data.get('phone')
        address = data.get('address')
        address_detail = data.get('address_detail')

        if not email:
            return jsonify({'status': 'fail', 'message': '이메일은 필수 입력 항목입니다.'}), 400

        success, error = update_user_info(user_id, email, birthdate, phone, address, address_detail)

        if not success:
            return jsonify({'status': 'fail', 'message': error}), 400

        updated_user = get_user_by_id(user_id)

        return jsonify({
            'status': 'success',
            'message': '사용자 정보가 성공적으로 수정되었습니다.',
            'data': updated_user
        }), 200
    except Exception as e:
        return jsonify({'status': 'fail', 'message': f'정보 수정 중 오류: {str(e)}'}), 500

# 7. 비밀번호 변경
@users_bp.route('/change-password', methods=['POST'])
@login_required
def change_password():
    try:
        user_id = session.get('user_id')

        # 이메일 인증 여부 확인
        if not session.get('email_verified'):
            return jsonify({'status': 'fail', 'message': '이메일 인증이 필요합니다.'}), 403

        data = request.get_json()
        current_password = data.get('current_password')
        new_password = data.get('new_password')

        success, error = change_user_password(user_id, current_password, new_password)

        if not success:
            return jsonify({'status': 'fail', 'message': error}), 400

        # 인증 완료 후 세션 값 제거 (선택)
        session.pop('email_verified', None)

        return jsonify({'status': 'success', 'message': '비밀번호가 변경되었습니다.'}), 200
    except Exception as e:
        return jsonify({'status': 'fail', 'message': str(e)}), 500

# 7-1. 2차인증메일
@users_bp.route('/send_verification_code', methods=['POST'])
def send_verification_code():
    email = request.form.get("email")

    if not email:
        return jsonify({"success": False, "message": "이메일 주소가 필요합니다."}), 400

    verification_code = str(random.randint(100000, 999999))
    session['verification_code'] = verification_code
    print(f"[DEBUG] 세션에 저장된 인증번호: {session['verification_code']}")

    msg = Message("닥터퓨처 이메일 인증번호", recipients=[email])
    msg.body = f"인증번호는 {verification_code} 입니다."

    try:
        mail.send(msg)
        return jsonify({"success": True, "message": "인증번호가 전송되었습니다."})
    except Exception as e:
        return jsonify({"success": False, "message": f"이메일 전송 실패: {str(e)}"}), 500

# 7-2. 인증번호 검증
@users_bp.route('/verify_code', methods=['POST'])
def verify_code():
    input_code = request.form.get('code')
    saved_code = session.get('verification_code')

    print("[DEBUG] 입력된 인증번호:", input_code)
    print("[DEBUG] 세션에 저장된 인증번호:", saved_code)

    if not saved_code or input_code != saved_code:
        return jsonify({'success': False, 'message': '인증번호가 일치하지 않습니다.'})

    # 검증 성공 → 인증 표시
    session['email_verified'] = True
    session.pop('verification_code', None)

    return jsonify({'success': True, 'message': '이메일 인증 성공!'})

# 8. 모바일 E2E 로그인
@users_bp.route('/E2E_login', methods=['POST', 'OPTIONS'])
@decrypt_request_json
def E2E_login():
    if request.method == 'OPTIONS':
        return '', 204

    try:
        from utils.decrypt_util import enable_response_encryption
        enable_response_encryption()  # 🔐 응답 암호화 활성화

        data = request._decrypted_json
        username = data.get('username', '').strip()
        password = data.get('password')

        if not username or not password:
            return jsonify({'status': 'fail', 'message': '아이디와 비밀번호를 입력하세요.'}), 400

        user_data, error = verify_user(username, password)

        if error:
            return jsonify({'status': 'fail', 'message': error}), 401

        session['user_id'] = user_data.get('id')
        session['username'] = user_data.get('username')

        response = {
            'status': 'success',
            'message': '로그인 성공',
            'data': user_data,
            'session': session.sid
        }

        if username.lower() == 'admin':
            response['redirect'] = '/admin'

        return jsonify(response), 200

    except Exception as e:
        return jsonify({'status': 'fail', 'message': f'로그인 오류: {str(e)}'}), 500
