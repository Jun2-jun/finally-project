from extensions import mysql
from utils.helpers import format_datetime

def get_all_reservations():
    """
    모든 예약 가져오기 (관리자 기능)
    """
    cur = mysql.connection.cursor()
    cur.execute("""
        SELECT id, user_id, name, phone, hospital, address, message, email, created_at, reservation_time 
        FROM reservations
    """)
    reservations = cur.fetchall()
    cur.close()
    
    # 날짜 형식 변환
    for res in reservations:
        res['created_at'] = format_datetime(res.get('created_at'))
    
    return reservations
 
def get_upcoming_reservations(limit=5):
    """
    대시보드용 최근 예약 가져오기
    """
    cur = mysql.connection.cursor()
    cur.execute("""
        SELECT id, name, hospital, created_at, reservation_time
        FROM reservations
        ORDER BY created_at DESC
        LIMIT %s
    """, (limit,))
    reservations = cur.fetchall()
    cur.close()
    
    for reservation in reservations:
        reservation['created_at'] = format_datetime(reservation.get('created_at'))
    
    return reservations

def create_reservation(name, phone, hospital, address, message='', email='', user_id=None, reservation_time=None):
    """
    새 예약 생성하기
    """
    # 디버깅 로그 추가
    print(f"🔍 DB 저장 시도: {name}, {phone}, {hospital}, {reservation_time}", flush=True)
    
    try:
        cur = mysql.connection.cursor()
        # NULL 값 처리를 위한 수정
        if user_id == "":
            user_id = None
            
        # reservation_time이 문자열인지 확인하고 적절히 처리
        if isinstance(reservation_time, str):
            # 이미 'YYYY-MM-DD HH:MM' 포맷이라고 가정
            pass
        elif reservation_time is None:
            reservation_time = datetime.now().strftime('%Y-%m-%d %H:%M')
            
        sql = """
            INSERT INTO reservations 
            (name, phone, hospital, address, message, email, user_id, created_at, reservation_time)
            VALUES (%s, %s, %s, %s, %s, %s, %s, NOW(), %s)
        """
        print(f"🔍 실행 SQL: {sql}", flush=True)
        print(f"🔍 매개변수: {(name, phone, hospital, address, message, email, user_id, reservation_time)}", flush=True)
        
        cur.execute(sql, (name, phone, hospital, address, message, email, user_id, reservation_time))
        mysql.connection.commit()
        reservation_id = cur.lastrowid
        cur.close()
        
        print(f"✅ DB 저장 성공: ID={reservation_id}", flush=True)
        return reservation_id
    except Exception as e:
        print(f"❌ DB 저장 중 오류: {str(e)}", flush=True)
        import traceback
        traceback.print_exc()  # 상세 에러 로그 출력
        raise

def get_reservation_stats():
    """
    대시보드용 예약 통계 가져오기
    """
    cur = mysql.connection.cursor()
    
    cur.execute("SELECT COUNT(*) as count FROM reservations")
    reservations_count = cur.fetchone()['count']
    
    cur.execute("SELECT COUNT(*) as count FROM reservations WHERE DATE(created_at) = CURDATE()")
    today_sessions = cur.fetchone()['count']
    
    cur.execute("SELECT COUNT(*) as count FROM reservations WHERE created_at >= NOW() - INTERVAL 1 DAY")
    new_bookings = cur.fetchone()['count']
    
    cur.close()
    
    return {
        'total': reservations_count,
        'today': today_sessions,
        'new': new_bookings
    }

def get_user_reservations(user_id):
    """
    특정 사용자의 모든 예약 가져오기
    """
    cur = mysql.connection.cursor()
    cur.execute("""
        SELECT id, name, phone, hospital, address, message, email, created_at, reservation_time 
        FROM reservations 
        WHERE user_id = %s
        ORDER BY created_at DESC
    """, (user_id,))
    reservations = cur.fetchall()
    cur.close()
    
    for res in reservations:
        res['created_at'] = format_datetime(res.get('created_at'))
        res['reservation_time'] = format_datetime(res.get('reservation_time'))
    
    return reservations
