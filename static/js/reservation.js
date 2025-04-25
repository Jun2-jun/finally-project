document.addEventListener('DOMContentLoaded', function() {
    // 폼 요소 가져오기
    const reservationForm = document.querySelector('form[action="/submit_reservation"]');
    
    if (!reservationForm) return; // 예약 폼이 없는 페이지에서는 실행하지 않음
    
    // 현재 날짜 설정 (오늘부터 예약 가능하도록)
    const reservationTimeInput = document.getElementById('reservation_time');
    if (reservationTimeInput) {
      const now = new Date();
      const year = now.getFullYear();
      const month = String(now.getMonth() + 1).padStart(2, '0');
      const day = String(now.getDate()).padStart(2, '0');
      const hours = String(now.getHours()).padStart(2, '0');
      const minutes = String(now.getMinutes()).padStart(2, '0');
      
      const minDateTime = `${year}-${month}-${day}T${hours}:${minutes}`;
      reservationTimeInput.setAttribute('min', minDateTime);
    }
    
    // 전화번호 입력 형식 제한 (자동으로 하이픈 추가)
    const phoneInput = document.getElementById('phone');
    if (phoneInput) {
      phoneInput.addEventListener('input', function(e) {
        let value = e.target.value.replace(/[^0-9]/g, ''); // 숫자만 남김
        
        if (value.length > 3 && value.length <= 7) {
          value = value.slice(0, 3) + '-' + value.slice(3);
        } else if (value.length > 7) {
          value = value.slice(0, 3) + '-' + value.slice(3, 7) + '-' + value.slice(7, 11);
        }
        
        e.target.value = value;
      });
    }
    
    // 폼 제출 이벤트 처리
    reservationForm.addEventListener('submit', function(e) {
      e.preventDefault(); // 기본 제출 동작 방지
      
      // 폼 유효성 검사
      if (!validateForm()) {
        return;
      }
      
      // 폼 데이터 수집
      const formData = {
        name: document.getElementById('name').value.trim(),
        phone: document.getElementById('phone').value.trim(),
        hospital: document.getElementById('hospital').value.trim(),
        address: document.getElementById('address').value.trim(),
        reservation_time: formatReservationTime(document.getElementById('reservation_time').value),
        message: document.getElementById('message').value.trim(),
        email: document.getElementById('email').value.trim()
      };
      
      // API 요청 보내기
      submitReservation(formData);
    });
    
    // 폼 유효성 검사 함수
    function validateForm() {
      const name = document.getElementById('name').value.trim();
      const phone = document.getElementById('phone').value.trim();
      const reservationTime = document.getElementById('reservation_time').value;
      
      // 이름 검사
      if (name === '') {
        alert('이름을 입력해주세요.');
        return false;
      }
      
      // 전화번호 검사
      const phoneRegex = /^01[0-9]-\d{3,4}-\d{4}$/;
      if (!phoneRegex.test(phone)) {
        alert('올바른 전화번호 형식을 입력해주세요. (예: 010-1234-5678)');
        return false;
      }
      
      // 예약 시간 검사
      if (reservationTime === '') {
        alert('예약 시간을 선택해주세요.');
        return false;
      }
      
      // 이메일 검사 (입력된 경우에만)
      const email = document.getElementById('email').value.trim();
      if (email !== '') {
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        if (!emailRegex.test(email)) {
          alert('올바른 이메일 형식을 입력해주세요.');
          return false;
        }
      }
      
      return true;
    }
    
    // 예약 시간 포맷 변환 (YYYY-MM-DDTHH:MM → YYYY-MM-DD HH:MM)
    function formatReservationTime(dateTimeLocal) {
      return dateTimeLocal.replace('T', ' ');
    }
    
    // API 요청 함수
    function submitReservation(formData) {
      // 로딩 표시 추가
      showLoading(true);
      
      // API 엔드포인트로 요청
      fetch('http://192.168.219.189:5002/api/reservations', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(formData)
      })
      .then(response => {
        if (!response.ok) {
          return response.json().then(data => {
            throw new Error(data.message || '서버 응답 오류');
          });
        }
        return response.json();
      })
      .then(data => {
        if (data.status === 'success') {
          // 성공 시 예약 완료 페이지로 이동
          showReservationSuccess(formData, data);
        } else {
          alert('예약 처리 중 오류가 발생했습니다: ' + data.message);
        }
      })
      .catch(error => {
        console.error('예약 제출 중 오류 발생:', error);
        alert('예약 제출 중 오류가 발생했습니다: ' + error.message);
      })
      .finally(() => {
        showLoading(false);
      });
    }
    
    // 예약 성공 화면 표시
    function showReservationSuccess(formData, responseData) {
      // 기존 컨텐츠 제거
      document.querySelector('.container').innerHTML = '';
      
      // 성공 화면 생성
      const successHtml = `
        <h1>🎉 예약이 완료되었습니다! 🎉</h1>
        
        <div class="details">
          <div class="detail-item"><strong>병원 이름</strong><span>${formData.hospital}</span></div>
          <div class="detail-item"><strong>병원 주소</strong><span>${formData.address}</span></div>
          <div class="detail-item"><strong>예약자 이름</strong><span>${formData.name}</span></div>
          <div class="detail-item"><strong>연락처</strong><span>${formData.phone}</span></div>
          <div class="detail-item"><strong>예약 시간</strong><span>${formData.reservation_time}</span></div>
          <div class="detail-item"><strong>요청 사항</strong><span>${formData.message || "없음"}</span></div>
          <div class="detail-item"><strong>이메일</strong><span>${formData.email || "없음"}</span></div>
        </div>
        
        <div class="btn-group">
          <a href="/" class="btn"><i data-lucide="home"></i> 홈으로</a>
          <a href="/find" class="btn"><i data-lucide="calendar-plus"></i> 다시 예약</a>
          <a href="/my_reservations" class="btn"><i data-lucide="clipboard-list"></i> 예약 내역</a>
          ${formData.email ? `<button id="send-email-btn" class="btn"><i data-lucide="mail"></i> 이메일 전송</button>` : ''}
        </div>
      `;
      
      document.querySelector('.container').innerHTML = successHtml;
      
      // 브라우저 이력에 추가 (뒤로 가기 버튼 작동하도록)
      window.history.pushState({}, "예약 완료", "/submit_reservation");
      
      // lucide 아이콘 다시 로드
      if (window.lucide) {
        window.lucide.createIcons();
      }
      
      // 이메일 전송 버튼 이벤트 리스너 추가
      const sendEmailBtn = document.getElementById('send-email-btn');
      if (sendEmailBtn) {
        sendEmailBtn.addEventListener('click', function() {
          sendEmail(formData);
        });
      }
      
      // 이메일이 자동 전송되었는지 표시
      if (responseData.email_sent) {
        const emailStatus = document.createElement('div');
        emailStatus.className = 'email-status success';
        emailStatus.innerHTML = '✅ 예약 정보가 이메일로 자동 전송되었습니다.';
        document.querySelector('.details').after(emailStatus);
      }
    }
    
    // 이메일 전송 API 요청 함수
    function sendEmail(formData) {
      if (!formData.email) {
        alert('이메일 주소가 필요합니다.');
        return;
      }
      
      showLoading(true);
      
      fetch('http://192.168.219.189:5002/api/reservations/send-email', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(formData)
      })
      .then(response => response.json())
      .then(data => {
        if (data.status === 'success') {
          alert('예약 정보가 이메일로 전송되었습니다.');
        } else {
          alert('이메일 전송에 실패했습니다: ' + (data.message || '알 수 없는 오류'));
        }
      })
      .catch(error => {
        console.error('이메일 전송 중 오류 발생:', error);
        alert('이메일 전송 중 오류가 발생했습니다.');
      })
      .finally(() => {
        showLoading(false);
      });
    }
    
    // 로딩 표시 함수
    function showLoading(isLoading) {
      if (isLoading) {
        // 로딩 요소가 이미 있는지 확인
        let loadingOverlay = document.getElementById('loading-overlay');
        
        if (!loadingOverlay) {
          // 로딩 요소 생성
          loadingOverlay = document.createElement('div');
          loadingOverlay.id = 'loading-overlay';
          loadingOverlay.style.cssText = `
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background-color: rgba(0, 0, 0, 0.5);
            display: flex;
            justify-content: center;
            align-items: center;
            z-index: 9999;
          `;
          
          const loadingSpinner = document.createElement('div');
          loadingSpinner.style.cssText = `
            width: 50px;
            height: 50px;
            border: 5px solid #f3f3f3;
            border-top: 5px solid #3498db;
            border-radius: 50%;
            animation: spin 1s linear infinite;
          `;
          
          // 애니메이션 스타일 추가
          const style = document.createElement('style');
          style.textContent = `
            @keyframes spin {
              0% { transform: rotate(0deg); }
              100% { transform: rotate(360deg); }
            }
          `;
          document.head.appendChild(style);
          
          loadingOverlay.appendChild(loadingSpinner);
          document.body.appendChild(loadingOverlay);
        } else {
          loadingOverlay.style.display = 'flex';
        }
      } else {
        // 로딩 요소 숨기기
        const loadingOverlay = document.getElementById('loading-overlay');
        if (loadingOverlay) {
          loadingOverlay.style.display = 'none';
        }
      }
    }
  });
  
  // 완료 페이지에서 이메일 전송 버튼 처리
  if (document.querySelector('form[action="/send_email"]')) {
    const emailForm = document.querySelector('form[action="/send_email"]');
    
    emailForm.addEventListener('submit', function(e) {
      e.preventDefault();
      
      const formData = {
        hospital: emailForm.querySelector('input[name="hospital"]').value,
        address: emailForm.querySelector('input[name="address"]').value,
        name: emailForm.querySelector('input[name="name"]').value,
        phone: emailForm.querySelector('input[name="phone"]').value,
        reservation_time: emailForm.querySelector('input[name="reservation_time"]').value,
        message: emailForm.querySelector('input[name="message"]').value,
        email: emailForm.querySelector('input[name="email"]').value
      };
      
      // 이메일 주소 체크
      if (!formData.email) {
        alert('이메일 주소가 필요합니다.');
        return;
      }
      
      // 로딩 표시
      const loadingOverlay = document.createElement('div');
      loadingOverlay.id = 'email-loading';
      loadingOverlay.style.cssText = `
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background-color: rgba(0, 0, 0, 0.5);
        display: flex;
        justify-content: center;
        align-items: center;
        z-index: 9999;
      `;
      
      const loadingText = document.createElement('div');
      loadingText.style.cssText = `
        background-color: white;
        padding: 20px;
        border-radius: 5px;
        box-shadow: 0 2px 10px rgba(0, 0, 0, 0.2);
      `;
      loadingText.textContent = '이메일 전송 중...';
      
      loadingOverlay.appendChild(loadingText);
      document.body.appendChild(loadingOverlay);
      
      // API 요청
      fetch('http://192.168.219.189:5002/api/reservations/send-email', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(formData)
      })
      .then(response => response.json())
      .then(data => {
        if (data.status === 'success') {
          alert('예약 정보가 이메일로 전송되었습니다.');
        } else {
          alert('이메일 전송에 실패했습니다: ' + (data.message || '알 수 없는 오류'));
        }
      })
      .catch(error => {
        console.error('이메일 전송 중 오류 발생:', error);
        alert('이메일 전송 중 오류가 발생했습니다.');
      })
      .finally(() => {
        // 로딩 제거
        document.getElementById('email-loading').remove();
      });
    });
  }