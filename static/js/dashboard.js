document.addEventListener('DOMContentLoaded', () => {
  const reservationCountEl = document.getElementById('reservation-count');
  const tbody = document.getElementById('reservation-table-body');

  // 초기 로딩 텍스트
  tbody.innerHTML = '<tr><td colspan="3" class="text-center">불러오는 중...</td></tr>';

  // 1. 로그인된 사용자 정보 가져오기
  fetch('http://192.168.219.131:5002/api/current-user', {
    method: 'GET',
    credentials: 'include'
  })
    .then(res => res.json())
    .then(userData => {
      if (userData.status === 'success' && userData.user) {
        const user = userData.user;
        const userId = user.id;

        // 유저 이름 등 표시
        document.getElementById('user-name').innerText = user.username || 'USER';
        document.getElementById('user-email').innerText = user.email || 'test01@naver.com';
        document.getElementById('welcome-name').innerText = `${user.username || 'Test Name'}님!`;

        // 2. 사용자별 예약 목록 가져오기
        return fetch(`http://192.168.219.131:5002/api/reservations/user/${userId}`, {
          method: 'GET',
          credentials: 'include'
        });
      } else {
        throw new Error('사용자 정보를 불러올 수 없습니다.');
      }
    })
    .then(res => res.json())
    .then(result => {
      tbody.innerHTML = '';

      if (result.status === 'success' && result.data && result.data.length > 0) {
        const reservations = result.data;
        reservationCountEl.textContent = reservations.length;

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
        reservationCountEl.textContent = '0';
        tbody.innerHTML = '<tr><td colspan="3" class="text-center">예약된 병원이 없습니다.</td></tr>';
      }
    })
    .catch(err => {
      console.error('예약 정보 로딩 실패:', err);
      reservationCountEl.textContent = '0';
      tbody.innerHTML = `<tr><td colspan="3" class="text-center text-danger">예약 정보를 불러오는 데 실패했습니다.</td></tr>`;
    });
});
