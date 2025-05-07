# routes/reserve.py
from flask import Blueprint, request, render_template

reserve_bp = Blueprint('reserve', __name__)

@reserve_bp.route('/reserve', methods=['GET', 'POST'])
def reserve():
    if request.method == 'POST':
        hospital_name = request.form.get('hospital_name')
        hospital_address = request.form.get('hospital_address')
        return render_template('submit_reservation.html',
                               hospital_name=hospital_name,
                               hospital_address=hospital_address)
    return render_template('reserve.html')
