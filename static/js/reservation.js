/**
 * 닥터퓨쳐 API 통신 모듈
 * - 예약 시스템과 API 서버(http://192.168.219.189:5002/api) 사이의 통신을 담당
 */

// API 서버 기본 URL
const API_BASE_URL = 'http://192.168.219.189:5002/api/reservations';

/**
 * 예약 정보를un API 서버로 전송하는 함수
 * @param {Object} reservationData - 예약 데이터 객체
 * @returns {Promise} - API 응답 프라미스
 */
async function sendReservationToAPI(reservationData) {
    try {
        console.log('API 서버로 예약 데이터 전송 시도:', reservationData);
        
        const response = await fetch(`${API_BASE_URL}/reservations`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(reservationData)
        });

        const data = await response.json();
        
        if (!response.ok) {
            console.error('API 서버 응답 오류:', data);
            throw new Error(data.message || '예약 처리 중 오류가 발생했습니다.');
        }
        
        console.log('API 서버 응답 성공:', data);
        return data;
    } catch (error) {
        console.error('예약 API 호출 실패:', error);
        throw error;
    }
}

/**
 * 예약 확인 이메일을 재전송하는 함수
 * @param {Object} emailData - 이메일 전송에 필요한 데이터
 * @returns {Promise} - API 응답 프라미스
 */
async function sendConfirmationEmail(emailData) {
    try {
        console.log('이메일 전송 요청:', emailData);
        
        const response = await fetch(`${API_BASE_URL}/reservations/send-email`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(emailData)
        });

        const data = await response.json();
        
        if (!response.ok) {
            throw new Error(data.message || '이메일 전송 중 오류가 발생했습니다.');
        }
        
        return data;
    } catch (error) {
        console.error('이메일 전송 API 호출 실패:', error);
        throw error;
    }
}

/**
 * 사용자의 예약 목록을 조회하는 함수
 * @param {number} userId - 사용자 ID
 * @returns {Promise} - API 응답 프라미스
 */
async function getUserReservations(userId) {
    try {
        const response = await fetch(`${API_BASE_URL}/reservations/user/${userId}`, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
            }
        });

        const data = await response.json();
        
        if (!response.ok) {
            throw new Error(data.message || '예약 조회 중 오류가 발생했습니다.');
        }
        
        return data;
    } catch (error) {
        console.error('예약 조회 API 호출 실패:', error);
        throw error;
    }
}