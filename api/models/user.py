from extensions import mysql
from utils.auth import hash_password, check_password
from utils.helpers import format_datetime
from MySQLdb.cursors import DictCursor

def get_all_users():
    """
    모든 사용자 가져오기 (관리자 기능)
    """
    cur = mysql.connection.cursor()
    cur.execute("SELECT id, username, email, birthdate, phone, address, address_detail FROM users")
    users = cur.fetchall()
    cur.close()
    return users

def get_user_by_id(user_id):
    cur = mysql.connection.cursor()
    cur.execute("SELECT id, username, email, password, birthdate, phone, address, address_detail, created_at FROM users WHERE id = %s", (user_id,))
    user = cur.fetchone()
    cur.close()

    if user:
        birth = user.get('birthdate')
        if birth:
            user['birthdate'] = birth.strftime('%Y-%m-%d') if not isinstance(birth, str) else birth

    return user


def get_user_by_username(username):
    """
    사용자명으로 사용자 가져오기
    """
    cur = mysql.connection.cursor()
    cur.execute("SELECT id, username, password, email, birthdate, phone, address, address_detail, admin FROM users WHERE username = %s", (username,))
    user = cur.fetchone()
    cur.close()
    return user

def create_user(username, password, email, birthdate=None, phone=None, address=None, address_detail=None):
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
        INSERT INTO users (username, password, email, birthdate, phone, address, address_detail, created_at)
        VALUES (%s, %s, %s, %s, %s, %s, %s, NOW())
    """, (username, hashed_password, email, birthdate, phone, address, address_detail))
    mysql.connection.commit()
    user_id = cur.lastrowid
    cur.close()
    
    return user_id, None

def verify_user(username, password):
    try:
        print("[DEBUG] 로그인 시도:", username)
        user = get_user_by_username(username)
        print("[DEBUG] 사용자 가져옴:", user)

        if not user:
            return None, "아이디 또는 비밀번호가 올바르지 않습니다."

        stored_password = user.get('password')
        print("[DEBUG] 저장된 해시:", stored_password)
        print("[DEBUG] 입력된 패스워드:", password)

        # bcrypt 비교 수행
        is_valid = False
        try:
            is_valid = check_password(stored_password, password)
        except Exception as e:
            print("[ERROR] bcrypt 비교 중 예외 발생:", str(e))

        if not (is_valid or stored_password == password):
            print("[DEBUG] 비밀번호 불일치")
            return None, "아이디 또는 비밀번호가 올바르지 않습니다."

        user_data = {
            'id': user.get('id'),
            'username': user.get('username'),
            'email': user.get('email'),
            'birthdate': format_datetime(user.get('birthdate')),
            'phone': user.get('phone'),
            'address': user.get('address'),
            'address_detail' : user.get('address_detail'),
            'admin' : user.get('admin')
        }

        print("[DEBUG] 로그인 성공:", user_data)
        return user_data, None

    except Exception as e:
        print("[FATAL ERROR] verify_user 실패:", str(e))
        return None

def delete_user(user_id):
    """
    사용자 계정을 삭제하는 함수
    """
    try:
        cur = mysql.connection.cursor()
        
        # 사용자와 관련된 데이터 삭제 (외래 키 제약조건 때문에 자식 테이블부터 삭제)
        # 예약 삭제
        cur.execute("DELETE FROM reservations WHERE user_id = %s", (user_id,))
        
        # Q&A 삭제
        cur.execute("DELETE FROM qna WHERE user_id = %s", (user_id,))
        
        # 공지사항 삭제
        cur.execute("DELETE FROM notice WHERE user_id = %s", (user_id,))
        
        # 마지막으로 사용자 삭제
        cur.execute("DELETE FROM users WHERE id = %s", (user_id,))
        
        mysql.connection.commit()
        deleted = cur.rowcount > 0
        cur.close()
        
        return deleted
    except Exception as e:
        # 오류 발생 시 롤백
        mysql.connection.rollback()
        raise e

def update_user_info(user_id, email, birthdate=None, phone=None, address=None, address_detail=None):
    """
    사용자 정보를 업데이트합니다.
    
    Args:
        user_id: 사용자 ID
        email: 이메일 주소(필수)
        birthdate: 생년월일(선택)
        phone: 전화번호(선택)
        address: 주소(선택)
        address_detail: 상세 주소(선택)
        
    Returns:
        (성공 여부, 오류 메시지)
    """
    try:
        # 이메일 중복 확인 (현재 사용자 제외)
        cur = mysql.connection.cursor()
        cur.execute("SELECT id FROM users WHERE email = %s AND id != %s", (email, user_id))
        existing_email = cur.fetchone()
        
        if existing_email:
            cur.close()
            return False, "이미 사용 중인 이메일입니다."
        
        # 업데이트할 필드와 값 준비
        update_fields = ["email = %s"]
        params = [email]
        
        if birthdate is not None:
            update_fields.append("birthdate = %s")
            params.append(birthdate)
            
        if phone is not None:
            update_fields.append("phone = %s")
            params.append(phone)
            
        if address is not None:
            update_fields.append("address = %s")
            params.append(address)
            
        if address_detail is not None:
            update_fields.append("address_detail = %s")
            params.append(address_detail)
            
        # 사용자 ID 파라미터 추가
        params.append(user_id)
        
        # UPDATE 쿼리 실행
        query = f"UPDATE users SET {', '.join(update_fields)} WHERE id = %s"
        cur.execute(query, params)
        mysql.connection.commit()
        
        updated = cur.rowcount > 0
        cur.close()
        
        if not updated:
            return False, "사용자 정보 업데이트 실패"
            
        return True, None
    except Exception as e:
        # 오류 발생 시 롤백
        mysql.connection.rollback()
        return False, f"사용자 정보 업데이트 오류: {str(e)}"
    
def change_user_password(user_id, current_password, new_password):
    """
    사용자의 비밀번호를 변경합니다.
    """
    try:
        # 현재 사용자 정보 가져오기
        cur = mysql.connection.cursor()
        cur.execute("SELECT password FROM users WHERE id = %s", (user_id,))
        user = cur.fetchone()
        
        if not user:
            cur.close()
            return False, "사용자를 찾을 수 없습니다."
        
        stored_password = user.get('password')
        
        # 현재 비밀번호 검증
        if not check_password(stored_password, current_password):
            cur.close()
            return False, "현재 비밀번호가 일치하지 않습니다."
        
        # 새 비밀번호 해싱
        hashed_new_password = hash_password(new_password)
        
        # 비밀번호 업데이트
        cur.execute("UPDATE users SET password = %s WHERE id = %s", 
                   (hashed_new_password, user_id))
        mysql.connection.commit()
        
        cur.close()
        return True, None
    except Exception as e:
        mysql.connection.rollback()
        return False, str(e)
