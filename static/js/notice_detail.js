document.addEventListener('DOMContentLoaded', function () {
    // ✅ 사용자 정보 불러오기
    fetch('http://192.168.219.131:5002/api/current-user', {
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
          if (userNameEl) userNameEl.innerText = data.user.username || 'USER';
          if (userEmailEl) userEmailEl.innerText = data.user.email || 'test01@naver.com';
        }
      })
      .catch(err => {
        console.error('사용자 정보 불러오기 실패:', err);
      });
  
    // ✅ 공지사항 ID 추출 (ex: /notice/post/4 → 4)
    const postId = window.location.pathname.split('/').pop();
  
    // ✅ 공지사항 상세 데이터 불러오기
    fetch(`http://192.168.219.131:5002/api/notices/${postId}`, {
      method: 'GET',
      credentials: 'include',
    })
      .then(res => res.json())
      .then(data => {
        if (data.status === 'success') {
          const post = data.data;
          document.getElementById('post-title').innerText = post.title;
          document.getElementById('post-created-at').innerText = `작성일: ${post.created_at}`;
          document.getElementById('post-content').innerHTML = post.comment; // HTML 포함 가능
        } else {
          document.getElementById('post-content').innerHTML = `<p class="text-danger">공지사항을 불러올 수 없습니다.</p>`;
        }
      })
      .catch(error => {
        console.error('공지사항 상세 불러오기 실패:', error);
        document.getElementById('post-content').innerHTML = `<p class="text-danger">오류가 발생했습니다.</p>`;
      });
  });
  
