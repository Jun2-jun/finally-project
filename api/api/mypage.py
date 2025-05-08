# api/mypage.py

from flask import Blueprint, render_template, session, redirect, url_for, jsonify, request
from models.user import get_user_by_id
from models.reservation import delete_reservation_by_id

mypage_bp = Blueprint('mypage', __name__, url_prefix='/mypage')

@mypage_bp.route('/', methods=['GET'])
def mypage():
    user_id = session.get('user_id')
    if not user_id:
        return redirect(url_for('users.api_login'))

    user = get_user_by_id(user_id)
    return render_template('mypage.html', user=user)

# 예약 삭제 API
@mypage_bp.route('/reservation/<int:reservation_id>', methods=['DELETE'])
def delete_reservation(reservation_id):
    try:
        # 예약 삭제 시도
        success = delete_reservation_by_id(reservation_id)
        
        if success:
            return jsonify({'message': '예약 삭제 완료'}), 200
        else:
            return jsonify({'message': '예약을 찾을 수 없습니다.'}), 404
    except Exception as e:
        print(f"삭제 요청 처리 중 오류: {str(e)}", flush=True)
        return jsonify({'message': '예약 삭제 처리 중 오류 발생'}), 500
