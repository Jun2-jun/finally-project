document.addEventListener('DOMContentLoaded', function () {
  // ✅ 사용자 정보 표시에만 사용
  fetch('http://192.168.219.248:5002/api/current-user', {
    method: 'GET',
    credentials: 'include',
    headers: {
      'Content-Type': 'application/json'
    }
  })
    .then(res => res.json())
    .then(data => {
      if (data.status === 'success') {
        const userNameEl = document.getElementById('user-name');
        const userEmailEl = document.getElementById('user-email');
        const welcomeNameEl = document.getElementById('welcome-name');

        if (userNameEl) userNameEl.innerText = data.user.username || 'USER';
        if (userEmailEl) userEmailEl.innerText = data.user.email || 'test01@naver.com';
        if (welcomeNameEl) welcomeNameEl.innerText = `${data.user.username || 'Test Name'}님!`;
      }
    })
    .catch(err => {
      console.error('사용자 정보 불러오기 실패:', err);
    });

  // ✅ 공지사항 목록 불러오기 (읽기 전용)
  fetch('http://192.168.219.248:5002/api/notices?page=1&per_page=10', {
    method: 'GET',
    credentials: 'include',
  })
    .then(res => res.json())
    .then(data => {
      if (data.status === 'success') {
        const notices = data.data.items;
        const tbody = document.getElementById('noticeTableBody');
        if (!tbody) return;
        tbody.innerHTML = '';

        notices.forEach((notice, index) => {
          const row = document.createElement('tr');
          row.classList.add('clickable-row');
          row.setAttribute('data-no', notice.id);
          row.innerHTML = `
            <td>${index + 1}</td>
            <td>${notice.title}</td>
            <td>${notice.author || '관리자'}</td>
            <td>${notice.created_at}</td>
            <td>${notice.views}</td>
          `;

          // ✅ 행 클릭 시 상세 페이지로 이동
          row.addEventListener('click', () => {
            window.location.href = `/notice/post/${notice.id}`;
          });

          tbody.appendChild(row);
        });
      } else {
        console.error('공지사항 불러오기 실패:', data.message);
      }
    })
    .catch(error => {
      console.error('공지사항 불러오기 에러:', error);
    });
});
