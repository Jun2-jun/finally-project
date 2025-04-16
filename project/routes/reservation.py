from flask import Blueprint, request
from modules.connection import mysql

reserve_bp = Blueprint('reserve', __name__)

@reserve_bp.route('/reserve', methods=['POST'])
def make_reservation():
    user_id = request.form.get('user_id')
    hospital_id = request.form.get('hospital_id')
    date = request.form.get('date')
    symptom = request.form.get('symptom', '')

    cur = mysql.connection.cursor()
    cur.execute(
        "INSERT INTO reservations(user_id, hospital_id, date, symptom_desc) VALUES(%s, %s, %s, %s)",
        (user_id, hospital_id, date, symptom)
    )
    mysql.connection.commit()
    cur.close()

    return "예약 완료! <a href='/'>홈으로</a>"
