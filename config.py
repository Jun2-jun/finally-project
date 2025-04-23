import os
from redis import Redis

# 애플리케이션 설정
class Config:
    # 일반 설정
    SECRET_KEY = os.environ.get('SECRET_KEY', 'default_secret_key')

    # MySQL 설정
    MYSQL_HOST = os.environ.get('MYSQL_HOST', 'localhost')
    MYSQL_USER = os.environ.get('MYSQL_USER', 'root')
    MYSQL_PASSWORD = os.environ.get('MYSQL_PASSWORD', '1234')
    MYSQL_DB = os.environ.get('MYSQL_DB', 'doctor_future')
    MYSQL_CURSORCLASS = 'DictCursor'

    # 세션 설정
    SESSION_TYPE = 'redis'
    SESSION_REDIS = Redis(host='localhost', port=6379)
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SECURE = True

    # 파일 업로드 설정
    UPLOAD_FOLDER = os.path.join(os.getcwd(), 'static', 'uploads')
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB 최대 업로드 크기

    # Flask-Mail 설정
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 587
    MAIL_USERNAME = 'doctorfutures2.0.0@gmail.com'
    MAIL_PASSWORD = 'tauq lacn quhn dbzz'
    MAIL_USE_TLS = True
    MAIL_USE_SSL = False
    MAIL_DEFAULT_SENDER = 'doctorfutures2.0.0@gmail.com'

    # AI API 설정
    GEMINI_API_KEY = os.environ.get('GEMINI_API_KEY', 'api키')


class DevelopmentConfig(Config):
    DEBUG = True
    SESSION_COOKIE_SECURE = False  # ✅ 로컬에선 False!
    SESSION_COOKIE_SAMESITE = 'Lax'  # ✅ 또는 'None' (CORS 환경이면)
    SESSION_COOKIE_DOMAIN = '192.168.219.62'  # ✅ 또는 정확한 IP 도메인

class ProductionConfig(Config):
    DEBUG = False
    SESSION_COOKIE_SECURE = False
    SESSION_COOKIE_SAMESITE = 'Lax' 


# 설정 딕셔너리
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
