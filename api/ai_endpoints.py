import os
import requests
from flask import Blueprint, jsonify, request, session
from utils.auth import login_required  # ✅ 로그인 강제 데코레이터
from extensions import mysql
from utils.xor import xor_encrypt, xor_decrypt, encode_base64, decode_base64

ai_bp = Blueprint('ai', __name__, url_prefix='/api/ai')

ENCRYPTION_KEY = 'secretkey'  # XOR 암호화 키

# POST /api/ai
@ai_bp.route('', methods=['POST'])
@login_required  # ✅ 반드시 로그인한 사용자만 허용
def gemini_api():
    try:
        data = request.get_json()
        prompt = data.get('prompt')
        
        if not prompt:
            return jsonify({
                'status': 'fail',
                'message': '프롬프트가 필요합니다.'
            }), 400

        user_id = session.get('user_id')  # 로그인 보장되니 세션에서 user_id 가져옴

        if prompt == '/비대면진료':
            # 유저 민감정보 조회
            patient_info = get_patient_info(user_id)
            if not patient_info:
                return jsonify({'status': 'fail', 'message': '민감정보가 없습니다.'}), 404

            # 개인 맞춤형 프롬프트 생성
            personalized_prompt = (
                f"당신은 전문 의료 상담 AI입니다. 다음은 환자의 건강 정보입니다.\n"
                f"혈액형: {patient_info['blood_type']}\n"
                f"키: {patient_info['height_cm']} cm\n"
                f"몸무게: {patient_info['weight_kg']} kg\n"
                f"알레르기: {patient_info['allergy_info']}\n"
                f"기존 질병 이력: {patient_info['past_illnesses']}\n"
                f"만성질환: {patient_info['chronic_diseases']}\n\n"
                "이 환자의 건강 상태를 고려하여 간단한 비대면 진단을 제공하세요."
            )

            result = call_gemini_api(personalized_prompt)

        elif prompt == '/예약조회':
            # 유저 예약 내역 조회
            reservations = get_reservations(user_id)
            if not reservations:
                return jsonify({'status': 'success', 'data': '예약 내역이 없습니다.'}), 200
            
            reservation_summary = "\n".join([
                f"- {r['hospital']} ({r['reservation_time']})" for r in reservations
            ])

            return jsonify({
                'status': 'success',
                'data': f'예약 내역입니다:\n{reservation_summary}'
            })

        else:
            # 일반 질문 (기본 의료 프롬프트 적용)
            medical_prompt = build_medical_prompt(prompt)
            result = call_gemini_api(medical_prompt)

        if 'error' in result:
            return jsonify({'status': 'fail', 'message': f'Gemini API 호출 중 오류: {result["error"]}'}), 500

        return jsonify({'status': 'success', 'data': result})

    except Exception as e:
        return jsonify({'status': 'fail', 'message': f'Gemini API 처리 중 예외 발생: {str(e)}'}), 500


# 🔥 유저 민감정보 조회
def get_patient_info(user_id):
    cur = mysql.connection.cursor()
    cur.execute("""
        SELECT blood_type, height_cm, weight_kg, allergy_info, past_illnesses, chronic_diseases
        FROM PatientSensitiveInfo
        WHERE user_id = %s
    """, (user_id,))
    row = cur.fetchone()
    cur.close()

    if not row:
        return None

    columns = ['blood_type', 'height_cm', 'weight_kg', 'allergy_info', 'past_illnesses', 'chronic_diseases']
    decrypted_data = {
        column: xor_decrypt(decode_base64(row[column]), ENCRYPTION_KEY)
        for column in columns
    }
    return decrypted_data


# 🔥 유저 예약내역 조회
def get_reservations(user_id):
    cur = mysql.connection.cursor()
    cur.execute("""
        SELECT hospital, reservation_time
        FROM reservations
        WHERE user_id = %s
        ORDER BY reservation_time DESC
    """, (user_id,))
    rows = cur.fetchall()
    cur.close()
    return rows


# 🔥 기본 의료 프롬프트 생성
def build_medical_prompt(prompt):
    return (
        "당신은 전문 의료 상담 AI입니다. 건강, 증상, 약 복용, 생활 습관 개선 관련 질문에만 답변하세요.\n\n"
        f"사용자 질문: {prompt}"
    )


# 🔥 Gemini API 호출
def call_gemini_api(prompt):
    api_key = os.environ.get('GEMINI_API_KEY', 'AIzaSyCNNvCkXPWQGKghFa7gMNVF1FPZm5-0V00')  # 기본 키 사용
    api_url = 'https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent'
    url = f"{api_url}?key={api_key}"

    headers = {
        'Content-Type': 'application/json'
    }

    data = {
        "contents": [{
            "parts": [{"text": prompt}]
        }]
    }

    try:
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        return {"error": str(e)}
