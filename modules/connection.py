from flask_mysqldb import MySQL

mysql = MySQL()

def init_db(app):
    app.config['MYSQL_HOST'] = 'localhost'
    app.config['MYSQL_USER'] = 'root'
    app.config['MYSQL_PASSWORD'] = 'yourpassword'  # ← 실제 비밀번호
    app.config['MYSQL_DB'] = 'hospital_app'
    mysql.init_app(app)
