from flask import jsonify
from . import api_bp
from models.reservation import get_reservation_stats
from models.user import get_all_users
from utils.auth import admin_required

# 대시보드 요약 정보 - dashboard.html용
@api_bp.route('/dashboard-info', methods=['GET'])
@admin_required
def dashboard_info():
    try:
        # 사용자 수 가져오기
        users = get_all_users()
        users_count = len(users)
        
        # 예약 통계 가져오기
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
            'message': f'대시보드 정보 조회 중 오류가 발생했습니다: {str(e)}'
        }), 500