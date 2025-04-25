/**
 * 닥터퓨쳐 API 통신 모듈
 * - 예약 시스템과 API 서버(http://192.168.219.189:5002/api) 사이의 통신을 담당
 */

// API 서버 기본 URL
const API_BASE_URL = 'http://192.168.219.189:5002/api/reservations';

/**
 * 예약 정보를 API 서버로 전송하는 함수
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
                'Accept': 'application/json',
                // CORS 이슈 해결을 위한 추가 헤더
                'Access-Control-Allow-Origin': '*'
            },
            mode: 'cors', // CORS 모드 명시적 설정
            credentials: 'include', // 필요시 'include'로 변경
            body: JSON.stringify(cleanReservationData(reservationData))
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
 * 예약 데이터를 정리하는 함수 (빈 문자열 및 특수 문자 처리)
 * @param {Object} data - 원본 예약 데이터
 * @returns {Object} - 정리된 예약 데이터
 */
function cleanReservationData(data) {
    // 데이터 복사본 생성
    const cleanedData = { ...data };
    
    // 빈 문자열 처리
    Object.keys(cleanedData).forEach(key => {
        // 빈 문자열이면 null로 설정 (API 요구사항에 따라)
        if (cleanedData[key] === '') {
            cleanedData[key] = null;
        }
        
        // 문자열 데이터에서 불필요한 이스케이프 처리 해제
        if (typeof cleanedData[key] === 'string') {
            // 템플릿 변수가 제대로 치환되지 않은 경우 처리 (예: "{{ name }}")
            if (cleanedData[key].includes('{{') && cleanedData[key].includes('}}')) {
                cleanedData[key] = null;
            }
            
            // 특수 문자 이스케이프 처리 해제
            cleanedData[key] = cleanedData[key].replace(/\\"/g, '"').replace(/\\'/g, "'");
        }
    });
    
    // reservation_time 형식 확인 및 처리
    if (cleanedData.reservation_time && typeof cleanedData.reservation_time === 'string') {
        // 이미 적절한 형식인지 확인 (YYYY-MM-DD HH:MM)
        if (!/^\d{4}-\d{2}-\d{2} \d{2}:\d{2}(:\d{2})?$/.test(cleanedData.reservation_time)) {
            // 날짜 형식이 맞지 않으면 현재 시간으로 설정
            const now = new Date();
            cleanedData.reservation_time = now.toISOString().slice(0, 16).replace('T', ' ');
        }
    }
    
    return cleanedData;
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
                'Accept': 'application/json',
                'Access-Control-Allow-Origin': '*'
            },
            mode: 'cors',
            body: JSON.stringify(cleanReservationData(emailData))
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
 * 연결 테스트 함수 - API 서버가 응답하는지 확인
 * @returns {Promise<boolean>} - 연결 성공 여부
 */
async function testApiConnection() {
    try {
        const controller = new AbortController();
        const timeoutId = setTimeout(() => controller.abort(), 5000); // 5초 타임아웃
        
        const response = await fetch(`${API_BASE_URL}/reservations/upcoming`, {
            method: 'GET',
            headers: {
                'Accept': 'application/json',
                'Access-Control-Allow-Origin': '*'
            },
            mode: 'cors',
            signal: controller.signal
        });
        
        clearTimeout(timeoutId);
        return response.ok;
    } catch (error) {
        console.error('API 서버 연결 테스트 실패:', error);
        return false;
    }
}

// 외부에서 사용할 수 있도록 함수 노출
window.sendReservationToAPI = sendReservationToAPI;
window.sendConfirmationEmail = sendConfirmationEmail;
window.testApiConnection = testApiConnection;