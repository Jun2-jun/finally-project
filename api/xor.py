from flask import Blueprint, request, jsonify, session
from utils.auth import login_required
from extensions import mysql
from utils.xor import xor_encrypt, xor_decrypt, encode_base64, decode_base64

patient_info_bp = Blueprint('patient_info', __name__, url_prefix='/api/patient')
ENCRYPTION_KEY = 'secretkey'

# POST: 민감정보 저장
@patient_info_bp.route('/info', methods=['POST'])
@login_required
def save_patient_info():
    data = request.get_json()

    # 프론트 필드 → DB 필드 매핑
    field_map = {
        'blood_type': 'blood_type',
        'height_cm': 'height_cm',
        'weight_kg': 'weight_kg',
        'allergy_info': 'allergy_info',
        'past_illnesses': 'past_illnesses',
        'chronic_diseases': 'chronic_diseases',
        'medications': 'medications',
        'smoking': 'smoking_status'
    }

    # 필수 필드 체크
    if not all(data.get(field, '').strip() != '' for field in field_map):
        return jsonify({'status': 'fail', 'message': '모든 필드를 입력해야 합니다.'}), 400

    user_id = session.get('user_id')
    if not user_id:
        return jsonify({'status': 'fail', 'message': '로그인이 필요합니다.'}), 401

    # 암호화 및 base64 인코딩
    encrypted_data = {
        db_field: encode_base64(xor_encrypt(str(data[form_field]), ENCRYPTION_KEY))
        for form_field, db_field in field_map.items()
    }

    cur = mysql.connection.cursor()
    cur.execute("SELECT user_id FROM PatientSensitiveInfo WHERE user_id = %s", (user_id,))
    exists = cur.fetchone()

    if exists:
        update_fields = ', '.join([f"{field}=%s" for field in encrypted_data])
        cur.execute(
            f"UPDATE PatientSensitiveInfo SET {update_fields} WHERE user_id = %s",
            list(encrypted_data.values()) + [user_id]
        )
    else:
        fields = ', '.join(encrypted_data.keys())
        placeholders = ', '.join(['%s'] * len(encrypted_data))
        cur.execute(
            f"INSERT INTO PatientSensitiveInfo (user_id, {fields}) VALUES (%s, {placeholders})",
            [user_id] + list(encrypted_data.values())
        )

    mysql.connection.commit()
    cur.close()

    return jsonify({'status': 'success', 'message': '건강 정보가 저장되었습니다.'}), 201

# GET: 민감정보 복호화 후 조회
@patient_info_bp.route('/info', methods=['GET'])
@login_required
def get_patient_info():
    user_id = session.get('user_id')
    if not user_id:
        return jsonify({'status': 'fail', 'message': '로그인이 필요합니다.'}), 401

    cur = mysql.connection.cursor()
    cur.execute("""
        SELECT blood_type, height_cm, weight_kg, allergy_info,
               past_illnesses, chronic_diseases, medications, smoking_status
        FROM PatientSensitiveInfo
        WHERE user_id = %s
    """, (user_id,))
    row = cur.fetchone()
    cur.close()

    if not row:
        return jsonify({'status': 'fail', 'message': '환자 정보를 찾을 수 없습니다.'}), 404

    try:
        decrypted_data = {
            'blood_type': xor_decrypt(decode_base64(row['blood_type']), ENCRYPTION_KEY) if row['blood_type'] else '',
            'height_cm': xor_decrypt(decode_base64(row['height_cm']), ENCRYPTION_KEY) if row['height_cm'] else '',
            'weight_kg': xor_decrypt(decode_base64(row['weight_kg']), ENCRYPTION_KEY) if row['weight_kg'] else '',
            'allergy_info': xor_decrypt(decode_base64(row['allergy_info']), ENCRYPTION_KEY) if row['allergy_info'] else '',
            'past_illnesses': xor_decrypt(decode_base64(row['past_illnesses']), ENCRYPTION_KEY) if row['past_illnesses'] else '',
            'chronic_diseases': xor_decrypt(decode_base64(row['chronic_diseases']), ENCRYPTION_KEY) if row['chronic_diseases'] else '',
            'medications': xor_decrypt(decode_base64(row['medications']), ENCRYPTION_KEY) if row['medications'] else '',
            'smoking': xor_decrypt(decode_base64(row['smoking_status']), ENCRYPTION_KEY) if row['smoking_status'] else ''
        }
    except Exception as e:
        return jsonify({'status': 'fail', 'message': f'복호화 실패: {str(e)}'}), 500

    return jsonify({'status': 'success', 'data': decrypted_data}), 200
