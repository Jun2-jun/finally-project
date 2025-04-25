/**
 * reservation.js - 닥터퓨쳐 예약 시스템 API 연결 모듈
 * 예약 관련 API와 통신하여 예약 처리 및 관리 기능을 제공합니다.
 */

// API 기본 URL 설정
const API_BASE_URL = 'http://192.168.219.189:5002/api/reservations';

/**
 * 예약 관련 API 기능을 제공하는 객체
 */
const ReservationAPI = {
  /**
   * 테스트 연결을 시도하는 함수
   * @returns {Promise} - API 응답 Promise 객체
   */
  testConnection: async function() {
    try {
      const response = await fetch(API_BASE_URL, {
        method: 'GET',
        credentials: 'include'
      });
      
      return await response.json();
    } catch (error) {
      console.error('API 연결 테스트 실패:', error);
      throw error;
    }
  },

  /**
   * 새로운 예약을 생성하는 함수
   * @param {Object} reservationData - 예약 정보 객체
   * @returns {Promise} - API 응답 Promise 객체
   */
  createReservation: async function(reservationData) {
    // 필수 필드 검증
    const requiredFields = ['name', 'phone', 'hospital', 'address', 'reservation_time'];
    for (const field of requiredFields) {
      if (!reservationData[field]) {
        throw new Error(`필수 입력 필드가 누락되었습니다: ${field}`);
      }
    }

    try {
      console.log('예약 요청 데이터:', reservationData);
      
      const response = await fetch(API_BASE_URL, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(reservationData),
        credentials: 'include' // 쿠키 포함 전송(세션 유지)
      });

      const result = await response.json();
      
      if (!response.ok) {
        throw new Error(result.message || '예약 생성 중 오류가 발생했습니다.');
      }
      
      return result;
    } catch (error) {
      console.error('예약 생성 실패:', error);
      throw error;
    }
  },

  /**
   * 예약 확인 이메일을 재전송하는 함수
   * @param {Object} emailData - 이메일 전송에 필요한 데이터
   * @returns {Promise} - API 응답 Promise 객체
   */
  sendConfirmationEmail: async function(emailData) {
    // 필수 이메일 필드 검증
    if (!emailData.email) {
      throw new Error('이메일 주소가 필요합니다.');
    }

    try {
      const response = await fetch(`${API_BASE_URL}/send-email`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(emailData),
        credentials: 'include'
      });

      const result = await response.json();
      
      if (!response.ok) {
        throw new Error(result.message || '이메일 전송 중 오류가 발생했습니다.');
      }
      
      return result;
    } catch (error) {
      console.error('이메일 전송 실패:', error);
      throw error;
    }
  },

  /**
   * 로그인한 사용자의 예약 목록을 조회하는 함수
   * @param {number} userId - 사용자 ID
   * @returns {Promise} - API 응답 Promise 객체
   */
  getUserReservations: async function(userId) {
    if (!userId) {
      throw new Error('사용자 ID가 필요합니다.');
    }

    try {
      const response = await fetch(`${API_BASE_URL}/user/${userId}`, {
        method: 'GET',
        credentials: 'include'
      });

      const result = await response.json();
      
      if (!response.ok) {
        throw new Error(result.message || '예약 조회 중 오류가 발생했습니다.');
      }
      
      return result.data;
    } catch (error) {
      console.error('사용자 예약 조회 실패:', error);
      throw error;
    }
  },

  /**
   * 최근 예정된 예약 목록을 조회하는 함수
   * @returns {Promise} - API 응답 Promise 객체
   */
  getUpcomingReservations: async function() {
    try {
      const response = await fetch(`${API_BASE_URL}/upcoming`, {
        method: 'GET',
        credentials: 'include'
      });

      const result = await response.json();
      
      if (!response.ok) {
        throw new Error(result.message || '예약 조회 중 오류가 발생했습니다.');
      }
      
      return result.data;
    } catch (error) {
      console.error('예정된 예약 조회 실패:', error);
      throw error;
    }
  }
};

/**
 * 예약 완료 페이지 관련 기능 모음
 */
const ReservationCompletePage = {
  /**
   * 예약 완료 페이지 초기화 함수
   */
  init: function() {
    // 이메일 전송 폼 제출 처리
    const emailForm = document.querySelector('form[action="/send_email"]');
    
    if (emailForm) {
      emailForm.addEventListener('submit', function(event) {
        event.preventDefault();
        
        // 폼 데이터 수집
        const formData = {
          hospital: emailForm.querySelector('input[name="hospital"]').value,
          address: emailForm.querySelector('input[name="address"]').value,
          name: emailForm.querySelector('input[name="name"]').value,
          phone: emailForm.querySelector('input[name="phone"]').value,
          reservation_time: emailForm.querySelector('input[name="reservation_time"]').value,
          message: emailForm.querySelector('input[name="message"]').value,
          email: emailForm.querySelector('input[name="email"]').value
        };
        
        // 이메일 전송 처리
        this.sendEmail(formData);
      }.bind(this));
    }
    
    // API 연결 테스트
    this.testAPIConnection();
  },
  
  /**
   * API 서버 연결 테스트 함수
   */
  testAPIConnection: async function() {
    try {
      console.log('API 서버 연결 테스트 중...');
      const result = await fetch('http://192.168.219.189:5002/api/reservations', {
        method: 'GET',
        credentials: 'include'
      });
      
      console.log('API 연결 테스트 결과:', await result.json());
    } catch (error) {
      console.error('API 서버 연결 실패:', error);
    }
  },

  /**
   * 예약 확인 이메일 전송 처리 함수
   * @param {Object} emailData - 이메일 데이터
   */
  sendEmail: async function(emailData) {
    try {
      const sendButton = document.querySelector('form[action="/send_email"] button');
      const originalText = sendButton.innerHTML;
      
      // 버튼 상태 업데이트
      sendButton.disabled = true;
      sendButton.innerHTML = '<i data-lucide="loader"></i> 전송 중...';
      lucide.createIcons(); // 아이콘 갱신
      
      // API 호출
      const result = await ReservationAPI.sendConfirmationEmail(emailData);
      
      // 성공 처리
      alert('예약 확인 이메일이 성공적으로 전송되었습니다.');
      
      // 버튼 상태 복원
      sendButton.disabled = false;
      sendButton.innerHTML = originalText;
      lucide.createIcons();
    } catch (error) {
      // 오류 처리
      alert(`이메일 전송 실패: ${error.message}`);
      
      // 버튼 상태 복원
      const sendButton = document.querySelector('form[action="/send_email"] button');
      sendButton.disabled = false;
      sendButton.innerHTML = '<i data-lucide="mail"></i> 이메일 전송';
      lucide.createIcons();
    }
  }
};

/**
 * 예약 폼 관련 기능 모음
 */
const ReservationForm = {
  /**
   * 예약 폼 초기화 함수
   * @param {string} formId - 예약 폼 요소의 ID
   */
  init: function(formId) {
    const form = document.getElementById(formId);
    
    if (!form) return;
    
    // API 연결 테스트
    this.testAPIConnection();
    
    form.addEventListener('submit', async function(event) {
      event.preventDefault();
      
      try {
        // 폼 데이터 수집
        const formData = new FormData(form);
        const reservationData = {};
        
        // FormData를 객체로 변환
        for (const [key, value] of formData.entries()) {
          reservationData[key] = value;
        }
        
        // 로그인한 사용자 ID가 있으면 추가 (세션에서 가져옴)
        const userId = this.getUserIdFromSession();
        if (userId) {
          reservationData.user_id = userId;
        }
        
        // 제출 버튼 상태 업데이트
        const submitButton = form.querySelector('button[type="submit"]');
        const originalText = submitButton.innerHTML;
        submitButton.disabled = true;
        submitButton.innerHTML = '예약 처리 중...';
        
        // API 호출
        const result = await ReservationAPI.createReservation(reservationData);
        
        // 성공 시 예약 완료 페이지로 이동
        window.location.href = `/reservation/complete?id=${result.data.reservation_id}`;
      } catch (error) {
        alert(`예약 실패: ${error.message}`);
        
        // 버튼 상태 복원
        const submitButton = form.querySelector('button[type="submit"]');
        submitButton.disabled = false;
        submitButton.innerHTML = originalText;
      }
    }.bind(this));
  },
  
  /**
   * API 서버 연결 테스트 함수
   */
  testAPIConnection: async function() {
    try {
      console.log('API 서버 연결 테스트 중...');
      const result = await fetch('http://192.168.219.189:5002/api/reservations', {
        method: 'GET',
        credentials: 'include'
      });
      
      console.log('API 연결 테스트 결과:', await result.json());
    } catch (error) {
      console.error('API 서버 연결 실패:', error);
    }
  },
  
  /**
   * 세션에서 사용자 ID를 가져오는 함수
   * (클라이언트 측에서 사용자 ID를 저장하는 방식에 따라 구현 필요)
   * @returns {number|null} - 사용자 ID 또는 null
   */
  getUserIdFromSession: function() {
    // 로컬 스토리지에서 사용자 정보 확인 (예시)
    const userInfo = localStorage.getItem('user_info');
    if (userInfo) {
      try {
        const user = JSON.parse(userInfo);
        return user.id;
      } catch (e) {
        console.error('사용자 정보 파싱 오류:', e);
      }
    }
    return null;
  }
};

/**
 * 예약 내역 페이지 관련 기능 모음
 */
const MyReservationsPage = {
  /**
   * 예약 내역 페이지 초기화 함수
   * @param {string} containerId - 예약 목록을 표시할 컨테이너 요소의 ID
   */
  init: function(containerId) {
    const container = document.getElementById(containerId);
    
    if (!container) return;
    
    // API 연결 테스트
    this.testAPIConnection();
    
    // 사용자 ID 확인
    const userId = this.getUserIdFromSession();
    
    if (userId) {
      this.loadUserReservations(userId, container);
    } else {
      container.innerHTML = '<p class="no-data">로그인이 필요합니다.</p>';
    }
  },
  
  /**
   * API 서버 연결 테스트 함수
   */
  testAPIConnection: async function() {
    try {
      console.log('API 서버 연결 테스트 중...');
      const result = await fetch('http://192.168.219.189:5002/api/reservations', {
        method: 'GET',
        credentials: 'include'
      });
      
      console.log('API 연결 테스트 결과:', await result.json());
    } catch (error) {
      console.error('API 서버 연결 실패:', error);
    }
  },
  
  /**
   * 사용자 예약 목록을 불러와 화면에 표시하는 함수
   * @param {number} userId - 사용자 ID
   * @param {HTMLElement} container - 예약 목록을 표시할 컨테이너 요소
   */
  loadUserReservations: async function(userId, container) {
    try {
      // 로딩 표시
      container.innerHTML = '<p class="loading">예약 내역을 불러오는 중입니다...</p>';
      
      // API 호출
      const reservations = await ReservationAPI.getUserReservations(userId);
      
      if (reservations.length === 0) {
        container.innerHTML = '<p class="no-data">예약 내역이 없습니다.</p>';
        return;
      }
      
      // 예약 목록 표시
      let html = '<ul class="reservation-list">';
      
      reservations.forEach(reservation => {
        html += `
          <li class="reservation-item">
            <div class="reservation-header">
              <h3>${reservation.hospital}</h3>
              <span class="reservation-date">${this.formatDateTime(reservation.reservation_time)}</span>
            </div>
            <div class="reservation-details">
              <p><strong>주소:</strong> ${reservation.address}</p>
              <p><strong>예약자:</strong> ${reservation.name}</p>
              <p><strong>연락처:</strong> ${reservation.phone}</p>
              ${reservation.message ? `<p><strong>요청사항:</strong> ${reservation.message}</p>` : ''}
            </div>
          </li>
        `;
      });
      
      html += '</ul>';
      container.innerHTML = html;
    } catch (error) {
      container.innerHTML = `<p class="error">예약 내역을 불러오는 중 오류가 발생했습니다: ${error.message}</p>`;
    }
  },
  
  /**
   * 날짜 및 시간 포맷팅 함수
   * @param {string} dateTimeStr - 날짜 및 시간 문자열
   * @returns {string} - 포맷팅된 날짜 및 시간 문자열
   */
  formatDateTime: function(dateTimeStr) {
    try {
      const date = new Date(dateTimeStr);
      return date.toLocaleString('ko-KR', {
        year: 'numeric',
        month: 'long',
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
      });
    } catch (e) {
      return dateTimeStr;
    }
  },
  
  /**
   * 세션에서 사용자 ID를 가져오는 함수
   * @returns {number|null} - 사용자 ID 또는 null
   */
  getUserIdFromSession: function() {
    // 로컬 스토리지에서 사용자 정보 확인 (예시)
    const userInfo = localStorage.getItem('user_info');
    if (userInfo) {
      try {
        const user = JSON.parse(userInfo);
        return user.id;
      } catch (e) {
        console.error('사용자 정보 파싱 오류:', e);
      }
    }
    return null;
  }
};

// DOMContentLoaded 이벤트에서 페이지 초기화
document.addEventListener('DOMContentLoaded', function() {
  // 페이지 로드 시 API 연결 테스트 실행
  console.log('페이지 로드됨, API 서버 연결 테스트 시작');
  fetch('http://192.168.219.189:5002/api/reservations', {
    method: 'GET',
    credentials: 'include'
  })
  .then(response => response.json())
  .then(data => {
    console.log('API 서버 연결 성공:', data);
  })
  .catch(error => {
    console.error('API 서버 연결 실패:', error);
  });
  
  // URL에 따라 적절한 초기화 함수 호출
  const pathname = window.location.pathname;
  
  if (pathname.includes('/reservation/complete')) {
    ReservationCompletePage.init();
  } else if (pathname.includes('/reservation/new') || pathname.includes('/find')) {
    ReservationForm.init('reservation-form');
  } else if (pathname.includes('/my_reservations')) {
    MyReservationsPage.init('reservations-container');
  }
});

// 전역 범위에서 ReservationAPI 객체 노출
window.ReservationAPI = ReservationAPI;