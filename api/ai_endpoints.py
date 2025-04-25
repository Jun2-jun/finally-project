# api/ai_endpoints.py

from flask import Blueprint, request, jsonify
from utils.ai import call_gemini_api
import os

# ✅ AI 전용 Blueprint 생성
ai_bp = Blueprint('ai', __name__, url_prefix='/api/ai')

# POST /api/ai
@ai_bp.route('', methods=['POST'])
def gemini_api():
    try:
        data = request.get_json()
        prompt = data.get('prompt')
        
        if not prompt:
            return jsonify({
                'status': 'fail',
                'message': '프롬프트가 필요합니다.'
            }), 400
            
        api_key = os.environ.get('GEMINI_API_KEY','AIzaSyCNNvCkXPWQGKghFa7gMNVF1FPZm5-0V00')  # 환경 변수에서 가져오기
        result = call_gemini_api(prompt, api_key)

        if 'error' in result:
            return jsonify({
                'status': 'fail',
                'message': f'Gemini API 호출 중 오류: {result["error"]}'
            }), 500

        return jsonify({
            'status': 'success',
            'data': result
        })

    except Exception as e:
        return jsonify({
            'status': 'fail',
            'message': f'Gemini API 처리 중 예외 발생: {str(e)}'
        }), 500
