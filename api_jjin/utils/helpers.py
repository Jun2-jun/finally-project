from datetime import datetime
import os
from werkzeug.utils import secure_filename
import json

# 날짜 형식 변환 함수
def format_datetime(dt):
    if isinstance(dt, datetime):
        return dt.strftime('%Y-%m-%d %H:%M:%S')
    return dt

# 파일 업로드 헬퍼
def save_uploaded_files(files, upload_folder):
    """
    업로드된 파일을 저장하고 파일 경로 목록 반환
    """
    file_paths = []
    
    for file in files:
        if file and file.filename != '':
            filename = secure_filename(file.filename)
            filepath = os.path.join(upload_folder, filename)
            file.save(filepath)
            # 웹 URL 형식으로 반환
            file_paths.append('/' + filepath.replace('\\', '/'))
    
    return file_paths

# JSON 문자열에서 이미지 URL 파싱
def parse_image_urls(image_urls_json):
    """
    JSON 문자열을 이미지 URL 목록으로 파싱
    """
    if not image_urls_json:
        return []
        
    try:
        return json.loads(image_urls_json)
    except:
        return []

# 쿼리 결과 페이지네이션
def paginate_results(query_results, page, per_page, total_count):
    """
    페이지네이션 정보 형식화
    """
    return {
        'items': query_results,
        'total': total_count,
        'page': page,
        'per_page': per_page,
        'total_pages': (total_count + per_page - 1) // per_page
    }