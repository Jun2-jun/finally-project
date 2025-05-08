document.addEventListener('DOMContentLoaded', () => {
  const reservationCountEl = document.getElementById('reservation-count');
  const tbody = document.getElementById('reservation-table-body');

  // 사이드바 유저 정보용 DOM
  const sidebarUsername = document.getElementById('sidebar-username');
  const sidebarEmail = document.getElementById('sidebar-email');
  const dropdownMenu = document.getElementById('dropdown-menu');

  const API_BASE = 'http://192.168.219.72:5002';

  if (tbody) {
    tbody.innerHTML = '<tr><td colspan="3" class="text-center">불러오는 중...</td></tr>';
  }

  fetch(`${API_BASE}/api/current-user`, {
    method: 'GET',
    credentials: 'include'
  })
    .then(res => res.json())
    .then(userData => {
      if (userData.status === 'success' && userData.user) {
        const user = userData.user;
        const userId = user.id;

        // ✅ 마이페이지용
        const userNameEl = document.getElementById('user-name');
        const userEmailEl = document.getElementById('user-email');
        const welcomeNameEl = document.getElementById('welcome-name');
        if (userNameEl) userNameEl.innerText = user.username || 'USER';
        if (userEmailEl) userEmailEl.innerText = user.email || 'test01@naver.com';
        if (welcomeNameEl) welcomeNameEl.innerText = `${user.username || '사용자'}님!`;

        // ✅ 사이드바 표시
        if (sidebarUsername) sidebarUsername.textContent = user.username;
        if (sidebarEmail) sidebarEmail.textContent = user.email;

        // ✅ 사이드바 이름 클릭 시 로그아웃 드롭다운 토글
        sidebarUsername.addEventListener('click', (e) => {
          e.stopPropagation();
          if (dropdownMenu) dropdownMenu.classList.toggle('hidden');
        });

        // 바깥 누르면 드롭다운 닫기
        window.addEventListener('click', () => {
          if (dropdownMenu) dropdownMenu.classList.add('hidden');
        });

        // ✅ 사용자 예약 정보 가져오기
        return fetch(`${API_BASE}/api/reservations/user/${userId}`, {
          method: 'GET',
          credentials: 'include'
        });
      } else {
        if (sidebarUsername) sidebarUsername.textContent = '로그인 필요';
        if (sidebarEmail) sidebarEmail.textContent = '';
        throw new Error('사용자 정보를 불러올 수 없습니다.');
      }
    })
    .then(res => res.json())
    .then(result => {
      if (!tbody || !reservationCountEl) return;

      tbody.innerHTML = '';

      if (result.status === 'success' && result.data?.length > 0) {
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
      if (reservationCountEl) reservationCountEl.textContent = '0';
      if (tbody) {
        tbody.innerHTML = `<tr><td colspan="3" class="text-center text-danger">예약 정보를 불러오는 데 실패했습니다.</td></tr>`;
      }
    });
});

// ✅ 로그아웃 요청 함수
function logout() {
  fetch('http://192.168.219.72:5002/api/users/logout', {
    method: 'POST',
    credentials: 'include'
  }).then(() => {
    alert('로그아웃 되었습니다.');
    window.location.href = '/login';
  });
}

// ✅ 섹션 스크롤 기능
function scrollToSection(id) {
  const el = document.getElementById(id);
  if (!el) return;

  const elementTop = el.getBoundingClientRect().top + window.scrollY;
  const scrollTarget = elementTop - (window.innerHeight / 2) + (el.offsetHeight / 2);

  window.scrollTo({
    top: scrollTarget,
    behavior: 'smooth'
  });
}
