from extensions import mysql
from utils.auth import hash_password, check_password
from utils.helpers import format_datetime

def get_all_users():
    """
    모든 사용자 가져오기 (관리자 기능)
    """
    cur = mysql.connection.cursor()
    cur.execute("SELECT id, username, email FROM users")
    users = cur.fetchall()
    cur.close()
    return users

def get_user_by_id(user_id):
    """
    ID로 사용자 가져오기
    """
    cur = mysql.connection.cursor()
    cur.execute("SELECT id, username, email, birthdate, phone, address, created_at FROM users WHERE id = %s", (user_id,))
    user = cur.fetchone()
    cur.close()
    
    if user:
        user['birthdate'] = format_datetime(user.get('birthdate'))
    
    return user

def get_user_by_username(username):
    """
    사용자명으로 사용자 가져오기
    """
    cur = mysql.connection.cursor()
    cur.execute("SELECT id, username, password, email, birthdate, phone, address FROM users WHERE username = %s", (username,))
    user = cur.fetchone()
    cur.close()
    return user

def create_user(username, password, email, birthdate=None, phone=None, address=None):
    """
    새 사용자 생성
    """
    # 사용자명 중복 확인
    cur = mysql.connection.cursor()
    cur.execute("SELECT id FROM users WHERE username = %s", (username,))
    existing_user = cur.fetchone()
    
    if existing_user:
        cur.close()
        return None, "이미 사용 중인 아이디입니다."
    
    # 비밀번호 해싱
    hashed_password = hash_password(password)
    
    # 사용자 삽입
    cur.execute("""
        INSERT INTO users (username, password, email, birthdate, phone, address, created_at)
        VALUES (%s, %s, %s, %s, %s, %s, NOW())
    """, (username, hashed_password, email, birthdate, phone, address))
    mysql.connection.commit()
    user_id = cur.lastrowid
    cur.close()
    
    return user_id, None

def verify_user(username, password):
    """
    사용자 자격 증명 확인
    """
    user = get_user_by_username(username)
    
    if not user:
        return None, "아이디 또는 비밀번호가 올바르지 않습니다."
    
    stored_password = user.get('password')
    
    # 개발용 - 해시 및 일반 비밀번호 모두 허용 (운영 환경에서는 제거 필요)
    if not (check_password(stored_password, password) or stored_password == password):
        return None, "아이디 또는 비밀번호가 올바르지 않습니다."
    
    # 응답용 사용자 데이터 형식화 (비밀번호 제외)
    user_data = {
        'id': user.get('id'),
        'username': user.get('username'),
        'email': user.get('email'),
        'birthdate': format_datetime(user.get('birthdate')),
        'phone': user.get('phone'),
        'address': user.get('address')
    }
    
    return user_data, None