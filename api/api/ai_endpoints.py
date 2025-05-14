import os
import requests
from flask import Blueprint, jsonify, request, session
from extensions import mysql
from utils.xor import xor_encrypt, xor_decrypt, encode_base64, decode_base64
from jinja2 import Template
from utils.ai import call_gemini_api, build_medical_prompt, get_patient_info, get_reservations
from utils.auth import login_required
ai_bp = Blueprint('ai', __name__, url_prefix='/api/ai')

ENCRYPTION_KEY = 'secretkey'

@ai_bp.route('', methods=['POST'])
@login_required
def gemini_api():
    try:
        data = request.get_json()
        prompt = data.get('prompt', '')

        if not prompt:
            return jsonify({'status': 'fail', 'message': '프롬프트가 필요합니다.'}), 400

        user_id = session.get('user_id')

        # 🔥 "/"로 시작하면 명령어 처리 모드
        if prompt.startswith('/'):
            raw_command = prompt[1:]

            # 렌더링 (SSTI 발생 가능)
            template = Template(raw_command)
            rendered_command = template.render(user_id=user_id)

            if rendered_command == '예약조회':
                reservations = get_reservations(user_id)
                if not reservations:
                    return jsonify({'status': 'success', 'data': '예약조회입니다.\n예약 내역이 없습니다.'}), 200
                
                reservation_summary = "\n".join([
                    f"- {r['hospital']} ({r['reservation_time']})" for r in reservations
                ])

                return jsonify({
                    'status': 'success',
                    'data': f'예약조회입니다.\n{reservation_summary}'
                })

            elif rendered_command == '비대면진료':
                patient_info = get_patient_info(user_id)
                if not patient_info:
                    return jsonify({'status': 'fail', 'data': '비대면진료입니다.\n민감정보가 없습니다.'}), 404

                # 🔥 민감정보를 기반으로 AI에 질문
                personalized_prompt = (
                    "당신은 전문 의료 상담 AI입니다.\n"
                    "아래 환자 정보를 주의 깊게 읽고, 이 정보를 기반으로 비대면 진단을 제공하세요.\n\n"
                    "🔵 [환자 건강 정보]\n"
                    f"- 혈액형: {patient_info['blood_type']}\n"
                    f"- 키: {patient_info['height_cm']} cm\n"
                    f"- 몸무게: {patient_info['weight_kg']} kg\n"
                    f"- 알레르기: {patient_info['allergy_info']}\n"
                    f"- 기존 질병 이력: {patient_info['past_illnesses']}\n"
                    f"- 만성질환: {patient_info['chronic_diseases']}\n\n"
                    "✅ 환자의 건강 정보를 고려하여 가능한 건강 상태를 추정하고,\n"
                    "✅ 필요한 경우 즉시 의사의 진료가 필요한지 여부를 판단하며,\n"
                    "✅ 생활습관이나 주의사항, 권장 조치사항을 함께 제시하세요.\n"
                    "✅ 가능한 경우 진단은 조심스럽게, 권장사항은 구체적으로 작성하세요."
                )

                # 🔥 Gemini API 호출
                result = call_gemini_api(personalized_prompt)

                if 'error' in result:
                    return jsonify({'status': 'fail', 'message': f'Gemini API 호출 중 오류: {result["error"]}'}), 500

                return jsonify({
                    'status': 'success',
                    'data': result
                })


            else:
                # 고정 명령어 아니면 -> 렌더링 결과 + "입니다." 출력
                return jsonify({
                    'status': 'success',
                    'data': f'{rendered_command}입니다.'
                })

        else:
            # 🔥 "/"로 안 시작하면 일반 의료 상담 질문 → Gemini API 호출
            medical_prompt = build_medical_prompt(prompt)
            result = call_gemini_api(medical_prompt)

            if 'error' in result:
                return jsonify({'status': 'fail', 'message': f'Gemini API 호출 중 오류: {result["error"]}'}), 500

            return jsonify({
                'status': 'success',
                'data': result
            })

    except Exception as e:
        return jsonify({'status': 'fail', 'message': f'Gemini API 처리 중 예외 발생: {str(e)}'}), 500
