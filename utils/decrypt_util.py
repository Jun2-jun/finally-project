# utils/decrypt_util.py

from functools import wraps
from flask import request, jsonify, g, current_app
from Crypto.Cipher import AES
import base64
import json

# 보안상 실제 서비스에서는 환경변수로 관리하세요
SECRET_KEY = b'H0sp1t4lAppS3cr3tK3y123456789012'  # 32 bytes
IV = b'H0sp1t4lAppIn1tV'  # 16 bytes

# ===== 🔓 복호화 =====
def decrypt_aes_base64(encrypted_text: str) -> str:
    cipher = AES.new(SECRET_KEY, AES.MODE_CBC, IV)
    decoded_data = base64.b64decode(encrypted_text)
    decrypted_data = cipher.decrypt(decoded_data)
    pad_len = decrypted_data[-1]
    return decrypted_data[:-pad_len].decode('utf-8')


# ===== 🔐 암호화 =====
def encrypt_aes_base64(plain_text: str) -> str:
    cipher = AES.new(SECRET_KEY, AES.MODE_CBC, IV)
    # PKCS7 패딩
    pad_len = 16 - (len(plain_text.encode('utf-8')) % 16)
    padded_text = plain_text + chr(pad_len) * pad_len
    encrypted_data = cipher.encrypt(padded_text.encode('utf-8'))
    return base64.b64encode(encrypted_data).decode('utf-8')


# ===== 📥 요청 복호화 데코레이터 =====
def decrypt_request_json(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        try:
            encrypted_payload = request.data.decode('utf-8')
            decrypted_json_str = decrypt_aes_base64(encrypted_payload)
            decrypted_json = json.loads(decrypted_json_str)
            # 복호화된 데이터 저장
            request._decrypted_json = decrypted_json
            return f(*args, **kwargs)
        except Exception as e:
            return jsonify({'status': 'fail', 'message': f'복호화 오류: {str(e)}'}), 400
    return decorated_function


# ===== 📤 응답 암호화 애프터훅 =====
def encrypt_response(response):
    try:
        # Content-Type이 JSON이고, 암호화 활성화된 경우만
        if response.content_type == 'application/json' and getattr(g, 'encrypt_response', False):
            original_data = response.get_data(as_text=True)
            encrypted_data = encrypt_aes_base64(original_data)
            response.set_data(encrypted_data)
            response.headers['Content-Type'] = 'text/plain'
            response.headers['X-Encrypted'] = 'true'
    except Exception as e:
        current_app.logger.error(f'응답 암호화 오류: {e}')
    return response


# ===== 🔘 뷰 함수에서 암호화 사용 요청 시 호출 =====
def enable_response_encryption():
    g.encrypt_response = True
