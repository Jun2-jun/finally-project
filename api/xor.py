from flask import Blueprint, request, jsonify, session
from utils.auth import login_required  # 기존 데코레이터 import
from extensions import mysql  # Flask-MySQLdb를 사용한다고 가정
from utils.xor import xor_encrypt, xor_decrypt, encode_base64, decode_base64

# Blueprint 생성
patient_info_bp = Blueprint('patient_info', __name__, url_prefix='/api/patient')

# 암호화 키 (실제 운영시에는 환경변수로 관리해야 함)
ENCRYPTION_KEY = 'secretkey'

@patient_info_bp.route('/info', methods=['POST'])
@login_required
def save_patient_info():
    data = request.get_json()
    
    # 필수 필드 검사
    required_fields = ['blood_type', 'height_cm', 'weight_kg', 'allergy_info', 'past_illnesses', 'chronic_diseases']
    if not all(field in data for field in required_fields):
        return jsonify({'status': 'fail', 'message': '모든 필드를 입력해야 합니다.'}), 400

    # 🔥 여기 수정!
    user_id = session.get('user_id')
    if not user_id:
        return jsonify({'status': 'fail', 'message': '로그인이 필요합니다.'}), 401

    # XOR 암호화 + Base64 인코딩
    encrypted_data = {
        field: encode_base64(xor_encrypt(str(data[field]), ENCRYPTION_KEY))
        for field in required_fields
    }

    cur = mysql.connection.cursor()

    # 기존 데이터 존재 여부 확인
    cur.execute("SELECT user_id FROM PatientSensitiveInfo WHERE user_id = %s", (user_id,))
    existing = cur.fetchone()

    if existing:
        # update
        cur.execute("""
            UPDATE PatientSensitiveInfo 
            SET blood_type=%s, height_cm=%s, weight_kg=%s, allergy_info=%s, past_illnesses=%s, chronic_diseases=%s
            WHERE user_id=%s
        """, (encrypted_data['blood_type'], encrypted_data['height_cm'], encrypted_data['weight_kg'],
              encrypted_data['allergy_info'], encrypted_data['past_illnesses'], encrypted_data['chronic_diseases'], user_id))
    else:
        # insert
        cur.execute("""
            INSERT INTO PatientSensitiveInfo (user_id, blood_type, height_cm, weight_kg, allergy_info, past_illnesses, chronic_diseases)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """, (user_id, encrypted_data['blood_type'], encrypted_data['height_cm'], encrypted_data['weight_kg'],
              encrypted_data['allergy_info'], encrypted_data['past_illnesses'], encrypted_data['chronic_diseases']))
    
    mysql.connection.commit()
    cur.close()

    return jsonify({'status': 'success', 'message': '환자 정보가 저장되었습니다.'}), 201

# 2. GET: 환자 민감정보 복호화 조회
@patient_info_bp.route('/info', methods=['GET'])
@login_required
def get_patient_info():
    # 🔥 세션에서 user_id 꺼내기
    user_id = session.get('user_id')
    if not user_id:
        return jsonify({'status': 'fail', 'message': '로그인이 필요합니다.'}), 401

    cur = mysql.connection.cursor()
    cur.execute("""
        SELECT blood_type, height_cm, weight_kg, allergy_info, past_illnesses, chronic_diseases
        FROM PatientSensitiveInfo
        WHERE user_id = %s
    """, (user_id,))
    row = cur.fetchone()
    cur.close()

    if not row:
        return jsonify({'status': 'fail', 'message': '환자 정보를 찾을 수 없습니다.'}), 404

    columns = ['blood_type', 'height_cm', 'weight_kg', 'allergy_info', 'past_illnesses', 'chronic_diseases']

    decrypted_data = {
        column: xor_decrypt(decode_base64(row[column]), ENCRYPTION_KEY)
        for column in columns
    }


    return jsonify({'status': 'success', 'data': decrypted_data}), 200
