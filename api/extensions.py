from flask_mysqldb import MySQL
from flask_cors import CORS
from flask_mail import Mail
from flask_session import Session
import os

# Flask 확장 초기화
mysql = MySQL()
mail = Mail()
session = Session()

# 업로드 폴더가 없으면 생성
def init_upload_folder(app):
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)