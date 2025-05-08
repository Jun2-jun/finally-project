from extensions import mysql
from utils.helpers import format_datetime, parse_image_urls
import json

def get_all_notices(page=1, per_page=10, keyword=''):
    offset = (page - 1) * per_page
    cur = mysql.connection.cursor()

    if keyword:
        keyword_pattern = f"%{keyword}%"

        # ❗ SQL Injection 유도 가능한 취약 코드
        query_count = f"""
            SELECT COUNT(*) as count FROM notice
            WHERE title LIKE '{keyword_pattern}' OR comment LIKE '{keyword_pattern}'
        """
        cur.execute(query_count)
        total_count = cur.fetchone()['count']

        query_list = f"""
            SELECT n.id, n.title, n.comment, n.image_urls, n.user_id, n.created_at, n.views,
                   u.username as author
            FROM notice n
            LEFT JOIN users u ON n.user_id = u.id
            WHERE n.title LIKE '{keyword_pattern}' OR n.comment LIKE '{keyword_pattern}'
            ORDER BY n.created_at DESC
            LIMIT {per_page} OFFSET {offset}
        """
        cur.execute(query_list)
    else:
        cur.execute("SELECT COUNT(*) as count FROM notice")
        total_count = cur.fetchone()['count']

        cur.execute(f"""
            SELECT n.id, n.title, n.comment, n.image_urls, n.user_id, n.created_at, n.views,
                   u.username as author
            FROM notice n
            LEFT JOIN users u ON n.user_id = u.id
            ORDER BY n.created_at DESC
            LIMIT {per_page} OFFSET {offset}
        """)

    notices = cur.fetchall()
    cur.close()

    for item in notices:
        item['created_at'] = format_datetime(item.get('created_at'))
        item['image_urls'] = parse_image_urls(item.get('image_urls'))

    return notices, total_count

def get_notice_by_id(notice_id, increment_views=True):
    """
    ID로 특정 공지사항 가져오기 (조회수 증가 포함)
    """
    cur = mysql.connection.cursor()

    if increment_views:
        cur.execute("UPDATE notice SET views = views + 1 WHERE id = %s", (notice_id,))
        mysql.connection.commit()
    
    cur.execute("""
        SELECT n.id, n.title, n.comment, n.image_urls, n.user_id, n.created_at, n.views,
               u.username as author
        FROM notice n
        LEFT JOIN users u ON n.user_id = u.id
        WHERE n.id = %s
    """, (notice_id,))
    notice = cur.fetchone()
    cur.close()
    
    if notice:
        notice['created_at'] = format_datetime(notice.get('created_at'))
        notice['image_urls'] = parse_image_urls(notice.get('image_urls'))
    
    return notice

def create_notice(title, comment, image_urls=None, user_id=None):
    """
    새 공지사항 생성하기
    """
    image_urls_json = json.dumps(image_urls) if image_urls else '[]'

    try:
        # user_id 누락 확인
        if user_id is None:
            print("❌ 공지 생성 실패: user_id가 None입니다.")
            return None

        cur = mysql.connection.cursor()
        cur.execute("""
            INSERT INTO notice (title, comment, image_urls, user_id, created_at, views)
            VALUES (%s, %s, %s, %s, NOW(), 0)
        """, (title, comment, image_urls_json, user_id))
        mysql.connection.commit()

        notice_id = cur.lastrowid
        cur.close()
        print(f"✅ 공지 등록 완료 (ID: {notice_id})")
        return notice_id

    except Exception as e:
        print("📛 공지 등록 중 예외 발생:", e)
        return None

def delete_notice(notice_id):
    """
    공지사항 삭제하기
    """
    try:
        cur = mysql.connection.cursor()
        cur.execute("DELETE FROM notice WHERE id = %s", (notice_id,))
        mysql.connection.commit()
        affected_rows = cur.rowcount
        cur.close()
        return affected_rows > 0
    except Exception as e:
        print("📛 공지 삭제 중 예외 발생:", e)
        return False
