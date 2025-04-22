from extensions import mysql
from utils.helpers import format_datetime, parse_image_urls
import json

def get_all_notices(page=1, per_page=10):
    """
    페이지네이션이 적용된 모든 공지사항 가져오기
    """
    offset = (page - 1) * per_page
    
    cur = mysql.connection.cursor()
    
    # 전체 개수 가져오기
    cur.execute("SELECT COUNT(*) as count FROM notice")
    total_count = cur.fetchone()['count']
    
    # 페이지 데이터 가져오기 (작성자 정보 포함)
    cur.execute("""
        SELECT n.id, n.title, n.comment, n.created_at, n.views, n.image_urls,
               n.user_id, u.username as author
        FROM notice n
        LEFT JOIN users u ON n.user_id = u.id
        ORDER BY n.created_at DESC
        LIMIT %s OFFSET %s
    """, (per_page, offset))
    notices = cur.fetchall()
    cur.close()
    
    # 데이터 형식 변환
    for item in notices:
        item['created_at'] = format_datetime(item.get('created_at'))
        item['image_urls'] = parse_image_urls(item.get('image_urls'))
    
    return notices, total_count

def get_notice_by_id(notice_id, increment_views=True):
    """
    ID로 특정 공지사항 가져오기
    조회수 증가 옵션 포함
    """
    cur = mysql.connection.cursor()
    
    # 요청시 조회수 증가
    if increment_views:
        cur.execute("UPDATE notice SET views = views + 1 WHERE id = %s", (notice_id,))
        mysql.connection.commit()
    
    # 공지사항 세부 정보 가져오기 (작성자 정보 포함)
    cur.execute("""
        SELECT n.id, n.title, n.comment, n.created_at, n.views, n.image_urls,
               n.user_id, u.username as author
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
    # image_urls를 JSON 문자열로 변환
    image_urls_json = json.dumps(image_urls) if image_urls else '[]'
    
    cur = mysql.connection.cursor()
    cur.execute("""
        INSERT INTO notice (title, comment, image_urls, user_id, created_at, views)
        VALUES (%s, %s, %s, %s, NOW(), 0)
    """, (title, comment, image_urls_json, user_id))
    mysql.connection.commit()
    notice_id = cur.lastrowid
    cur.close()
    
    return notice_id

def delete_notice(notice_id):
    """
    공지사항 삭제하기
    """
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM notice WHERE id = %s", (notice_id,))
    mysql.connection.commit()
    affected_rows = cur.rowcount
    cur.close()
    
    return affected_rows > 0