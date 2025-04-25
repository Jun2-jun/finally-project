// qna_detail.js
console.log("✅ qna_detail.js 로딩됨");

document.addEventListener('DOMContentLoaded', function () {
  // 사용자 정보 표시
  fetch('http://192.168.219.189:5002/api/current-user', {
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

  const postId = window.location.pathname.split('/').pop();

  // Q&A 상세 정보
  fetch(`http://192.168.219.189:5002/api/qna/${postId}`, {
    method: 'GET',
    credentials: 'include'
  })
    .then(res => res.json())
    .then(data => {
      if (data.status === 'success') {
        const post = data.data;
        document.getElementById('post-title').innerText = post.title;
        document.getElementById('post-author').innerText = post.writer || '익명';
        document.getElementById('post-date').innerText = post.created_at;
        document.getElementById('post-content').innerHTML = post.comment;
      } else {
        document.getElementById('post-title').innerText = '게시글이 없습니다.';
        document.getElementById('post-content').innerText = data.message || '';
      }
    })
    .catch(err => {
      console.error('❌ Q&A 상세 로딩 실패:', err);
      document.getElementById('post-title').innerText = '오류 발생';
      document.getElementById('post-content').innerText = '서버로부터 데이터를 가져오지 못했습니다.';
    });

  loadComments(postId);
});

// ✅ 댓글 조회 함수
function loadComments(postId) {
  fetch(`http://192.168.219.189:5002/api/qna/${postId}/comments`, {
    method: 'GET',
    credentials: 'include'
  })
    .then(res => res.json())
    .then(data => {
      const list = document.getElementById('comment-list');
      list.innerHTML = '';
      data.forEach(comment => {
        const el = document.createElement('div');
        el.className = 'mb-3';
        el.innerHTML = `
          <strong>${comment.username}</strong>
          <small class="text-muted ms-2">${comment.created_at}</small>
          <p class="mb-0">${comment.comment}</p>
          <hr>
        `;
        list.appendChild(el);
      });
    });
}

// ✅ 댓글 등록 함수
function submitComment() {
  const comment = document.getElementById('comment-input').value.trim();
  const postId = window.location.pathname.split('/').pop();

  if (!comment) {
    alert('댓글을 입력해주세요.');
    return;
  }

  const formData = new FormData();
  formData.append('comment', comment);

  fetch(`http://192.168.219.189:5002/api/qna/${postId}/comments`, {
    method: 'POST',
    body: formData,
    credentials: 'include'
  })
    .then(res => res.json())
    .then(data => {
      if (data.status === 'success') {
        document.getElementById('comment-input').value = '';
        loadComments(postId);
      } else {
        alert(data.message || '댓글 등록 실패');
      }
    })
    .catch(err => {
      console.error('댓글 등록 중 오류:', err);
      alert('서버 오류로 댓글을 등록할 수 없습니다.');
    });
}
