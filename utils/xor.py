import base64

# XOR 암호화
def xor_encrypt(plain_text, key):
    encrypted = []
    key_len = len(key)
    for i, c in enumerate(plain_text):
        encrypted.append(chr(ord(c) ^ ord(key[i % key_len])))
    return ''.join(encrypted)

# XOR 복호화 (XOR은 대칭 알고리즘이라 함수는 같다)
def xor_decrypt(cipher_text, key):
    return xor_encrypt(cipher_text, key)

# Base64 인코딩 (바이너리 데이터를 안전하게 문자열로 변환)
def encode_base64(text):
    return base64.b64encode(text.encode()).decode()

# Base64 디코딩 (문자열을 다시 바이너리로 복원)
def decode_base64(text):
    return base64.b64decode(text.encode()).decode()
