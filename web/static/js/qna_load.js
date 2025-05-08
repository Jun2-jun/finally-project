document.addEventListener('DOMContentLoaded', () => {
  const tbody = document.querySelector('.notice-table tbody');
  const welcomeNameEl = document.getElementById('welcome-name');
  const userNameEl = document.getElementById('user-name');
  const userEmailEl = document.getElementById('user-email');

  // 초기화
  if (tbody) {
    tbody.innerHTML = '<tr><td colspan="6" class="text-muted py-4">불러오는 중...</td></tr>';
  }

  // 사용자 정보 불러오기
  fetch('http://192.168.219.248:5002/api/current-user', {
    method: 'GET',
    credentials: 'include'
  })
  .then(res => res.json())
  .then(data => {
    if (data.status === 'success') {
      const username = data.user.username || 'USER';
      const email = data.user.email || 'test01@naver.com';
      if (userNameEl) userNameEl.innerText = username;
      if (userEmailEl) userEmailEl.innerText = email;
      if (welcomeNameEl) welcomeNameEl.innerText = `${username}님!`;
    }
  })
  .catch(err => {
    console.error('❌ 사용자 정보 로딩 실패:', err);
  });

  // QnA 목록 불러오기
  fetch('http://192.168.219.248:5002/api/qna/?page=1&per_page=10', {
    method: 'GET',
    credentials: 'include'
  })
  .then(res => res.json())
  .then(data => {
    if (!tbody) return;

    tbody.innerHTML = '';
    if (data.status === 'success' && data.data?.items && data.data.items.length > 0) {
      data.data.items.forEach((post, idx) => {
        const row = document.createElement('tr');
        row.classList.add('clickable-row');
        row.setAttribute('data-no', post.id);

        row.innerHTML = `
          <td class="delete-checkbox-column" style="display: none;">
            <input type="checkbox" class="delete-checkbox" value="${post.id}">
          </td>
          <td>${idx + 1}</td>
          <td>
            <a href="/qna/post/${post.id}" style="text-decoration: none; color: inherit;">
              ${post.title}
            </a>
          </td>
          <td>${post.writer || '알 수 없음'}</td>
          <td>${post.created_at}</td>
        `;

        tbody.appendChild(row);
      });
    } else {
      tbody.innerHTML = '<tr><td colspan="6" class="text-muted py-4">질문이 없습니다.</td></tr>';
    }
  })
  .catch(err => {
    console.error('❌ Q&A 목록 로딩 실패:', err);
    if (tbody) {
      tbody.innerHTML = '<tr><td colspan="6" class="text-danger py-4">목록을 불러오는 데 실패했습니다.</td></tr>';
    }
  });
});
