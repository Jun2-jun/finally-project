console.log("✅ qna_detail.js 로딩됨");

document.addEventListener('DOMContentLoaded', function () {
  const postId = window.location.pathname.split('/').pop();
  let loggedInUsername = null;
  let postAuthor = null;

  // 1. 로그인 사용자 정보 확인
  fetch('http://192.168.219.248:5002/api/current-user', {
    method: 'GET',
    credentials: 'include'
  })
    .then(res => res.json())
    .then(data => {
      if (data.status === 'success') {
        loggedInUsername = data.user.username;
      }
    });

  // 2. 게시글 상세 정보 가져오기
  fetch(`http://192.168.219.248:5002/api/qna/${postId}`, {
    method: 'GET',
    credentials: 'include'
  })
    .then(res => res.json())
    .then(data => {
      if (data.status === 'success') {
        const post = data.data;
        postAuthor = post.writer;

        document.getElementById('post-title').innerText = post.title;
        document.getElementById('post-author').innerText = post.writer || '익명';
        document.getElementById('post-date').innerText = post.created_at;
        document.getElementById('post-content').innerHTML = post.comment;

        // 3. 작성자와 로그인 사용자가 같으면 삭제 버튼 표시
        if (loggedInUsername && loggedInUsername === postAuthor) {
          document.getElementById('delete-button').classList.remove('d-none');
        }
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

// ✅ 댓글 불러오기
function loadComments(postId) {
  fetch(`http://192.168.29.134:5002/api/qna/${postId}/comments`, {
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

// ✅ 댓글 등록
function submitComment() {
  const comment = document.getElementById('comment-input').value.trim();
  const postId = window.location.pathname.split('/').pop();

  if (!comment) {
    alert('댓글을 입력해주세요.');
    return;
  }

  const formData = new FormData();
  formData.append('comment', comment);

  fetch(`http://192.168.29.134:5002/api/qna/${postId}/comments`, {
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

// ✅ 게시글 삭제 요청
function deletePost() {
  if (!confirm("정말 이 게시글을 삭제하시겠습니까?")) return;

  const postId = window.location.pathname.split('/').pop();

  fetch(`http://192.168.219.248:5002/api/qna/${postId}/delete`, {
    method: 'POST',
    credentials: 'include'
  })
    .then(res => res.json())
    .then(data => {
      if (data.status === 'success') {
        alert('게시글이 삭제되었습니다.');
        window.location.href = '/qna';
      } else {
        alert(data.message || '삭제 실패');
      }
    })
    .catch(err => {
      console.error('삭제 요청 오류:', err);
      alert('서버 오류로 삭제할 수 없습니다.');
    });
}
