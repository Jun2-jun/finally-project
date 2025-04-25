document.addEventListener('DOMContentLoaded', () => {
  console.log("🔥 유저 정보 API 호출 시작");  
  fetch('http://192.168.219.189:5002/api/current-user', {
      method: 'GET',
      credentials: 'include'
    })
      .then(res => res.json())
      .then(data => {
        if (data.status === 'success') {
          document.getElementById('user-name').innerText = data.user.username || 'USER';  // ✅ 수정
          document.getElementById('user-email').innerText = data.user.email || 'test01@naver.com';
          document.getElementById('welcome-name').innerText = `${data.user.username || 'Test Name'}님!`;  // ✅ 수정
        }
      })
      .catch(err => {
        console.error('사용자 정보 불러오기 실패:', err);
      });
});


document.addEventListener('DOMContentLoaded', () => {
  console.log("📅 예약 정보 fetch 시작");
  // 예약 목록 가져오기
  const reservationCountEl = document.getElementById('reservation-count');
  const tbody = document.getElementById('reservation-table-body');
  
  // Loading indicator
  tbody.innerHTML = '<tr><td colspan="3" class="text-center">불러오는 중...</td></tr>';
    
  fetch('http://192.168.219.189:5002/api/reservations/upcoming', {
    method: 'GET',
    credentials: 'include',  // 세션 쿠키를 포함하여 요청
    headers: {
      'Content-Type': 'application/json',
      'Accept': 'application/json'
    }
  })
    .then(response => {
      console.log('API Response Status:', response.status);
      if (!response.ok) {
        throw new Error(`API 요청 실패: ${response.status}`);
      }
      return response.json();
    })
    .then(result => {
      console.log('API Response Data:', result);
      tbody.innerHTML = '';
      // 예약 정보가 있는 경우
      if (result.status === 'success' && result.data && result.data.length > 0) {
        const reservations = result.data;
      
        // 예약 개수 표시
        reservationCountEl.textContent = reservations.length;
        
        // 테이블에 예약 목록 표시
        reservations.forEach((reservation, index) => {
          const row = `
            <tr>
              <td>${index + 1}</td>
              <td>${reservation.hospital}</td>
              <td>${reservation.created_at}</td>
            </tr>
          `;
          tbody.insertAdjacentHTML('beforeend', row);
        });
      } else {
        // 예약 정보가 없는 경우
        reservationCountEl.textContent = '0';
        tbody.innerHTML = '<tr><td colspan="3" class="text-center">예약된 병원이 없습니다.</td></tr>';
      }
    })
    .catch(error => {
      console.error('예약 정보를 가져오는 중 오류 발생:', error);
      reservationCountEl.textContent = '0';
      tbody.innerHTML = `<tr><td colspan="3" class="text-center text-danger">예약 정보를 불러오는 데 실패했습니다: ${error.message}</td></tr>`;
    });
});
