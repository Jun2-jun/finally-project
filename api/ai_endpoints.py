import os
import requests
from flask import Blueprint, jsonify, request, session
from utils.auth import login_required  # ✅ 로그인 강제 데코레이터

from utils.ai import call_gemini_api, build_medical_prompt, get_patient_info, get_reservations
ai_bp = Blueprint('ai', __name__, url_prefix='/api/ai')

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


