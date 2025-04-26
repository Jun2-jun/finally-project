# api/dashboard.py

from flask import Blueprint, jsonify
from models.reservation import get_reservation_stats
from models.user import get_all_users
from utils.auth import admin_required

# 기능별 Blueprint 생성
dashboard_bp = Blueprint('dashboard', __name__, url_prefix='/api/dashboard')

# 관리자 전용 대시보드 정보
@dashboard_bp.route('/info', methods=['GET'])
@admin_required
def dashboard_info():
    try:
        users = get_all_users()
        users_count = len(users)
        reservation_stats = get_reservation_stats()

        return jsonify({
            'status': 'success',
            'data': {
                'users': users_count,
                'reservations': reservation_stats['total'],
                'new_bookings': reservation_stats['new'],
                'today_sessions': reservation_stats['today']
            }
        })
    except Exception as e:
        return jsonify({
            'status': 'fail',
            'message': f'대시보드 정보 조회 중 오류: {str(e)}'
        }), 500
