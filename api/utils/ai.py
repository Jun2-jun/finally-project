from extensions import mysql
from utils.xor import xor_encrypt, xor_decrypt, encode_base64, decode_base64
import os
import requests


ENCRYPTION_KEY = 'secretkey'  # XOR 암호화 키

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

def call_local_ai_api(prompt: str) -> str | dict:
    try:
        response = requests.post(
            "http://10.1.30.61:8001/generate",  # ← 실제 AI 서버 IP 또는 localhost
            json={"question": prompt},
            timeout=15
        )
        response.raise_for_status()
        return response.json().get("answer", "AI 응답이 비어 있습니다.")
    except requests.exceptions.RequestException as e:
        return {"error": str(e)}
