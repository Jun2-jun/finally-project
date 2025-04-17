from flask import Blueprint, render_template, request

submit_bp = Blueprint('submit', __name__)

@submit_bp.route('/submit_reservation', methods=['POST'])
def submit_reservation():
    # form으로부터 데이터 받기
    hospital = request.form.get('hospital')
    address = request.form.get('address')
    name = request.form.get('name')
    phone = request.form.get('phone')
    message = request.form.get('message')
    email = request.form.get('email')

    return render_template("submit_reservation.html",
                           hospital=hospital,
                           address=address,
                           name=name,
                           phone=phone,
                           message=message,
                           email=email)
