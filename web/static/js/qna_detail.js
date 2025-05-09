console.log("✅ qna_detail.js 로딩됨");

document.addEventListener('DOMContentLoaded', function () {
  const postId = window.location.pathname.split('/').pop();
  let loggedInUsername = null;
  let postAuthor = null;
  const serverIP = document.body.dataset.serverIp;
  // 1. 로그인 사용자 정보 확인
  fetch(`${serverIP}/api/current-user`, {
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
  fetch(`${serverIP}/api/qna/${postId}`, {
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
  fetch(`${serverIP}/api/qna/${postId}/comments`, {
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

  fetch(`${serverIP}/api/qna/${postId}/comments`, {
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

  fetch(`${serverIP}/api/qna/${postId}/delete`, {
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


function submitComment() {
  const commentInput = document.getElementById('comment-input');
  const comment = commentInput.value.trim();
  const postId = window.location.pathname.split('/').pop();

  if (!comment) return alert('댓글을 입력하세요.');

  const formData = new FormData();
  formData.append('comment', comment);

  fetch(`${serverIP}/api/qna/${postId}/comments`, {
    method: 'POST',
    body: formData,
    credentials: 'include'
  })
    .then(res => res.json())
    .then(data => {
      if (data.status === 'success') {
        commentInput.value = '';
        loadComments(postId);
      } else {
        alert(data.message || '댓글 등록 실패');
      }
    })
    .catch(err => {
      console.error('댓글 등록 중 오류:', err);
    });
}

function submitReply(parentId) {
  const replyInput = document.getElementById(`reply-comment-${parentId}`);
  const replyComment = replyInput.value.trim();
  const postId = window.location.pathname.split('/').pop();

  if (!replyComment) return alert('대댓글을 입력해주세요.');

  const formData = new FormData();
  formData.append('comment', replyComment);
  formData.append('parent_id', parentId);

  fetch(`${serverIP}/api/qna/${postId}/comments`, {
    method: 'POST',
    body: formData,
    credentials: 'include'
  })
    .then(res => res.json())
    .then(data => {
      if (data.status === 'success') {
        loadComments(postId);
      } else {
        alert(data.message || '대댓글 등록 실패');
      }
    })
    .catch(err => {
      console.error('대댓글 등록 중 오류:', err);
    });
}

function showReplyInput(commentId) {
  const replyInput = document.getElementById(`reply-input-${commentId}`);
  replyInput.style.display = replyInput.style.display === 'none' ? 'block' : 'none';
}

function loadComments(postId) {
  fetch(`${serverIP}/api/qna/${postId}/comments`, {
    method: 'GET',
    credentials: 'include'
  })
    .then(res => res.json())
    .then(comments => {
      const list = document.getElementById('comment-list');
      list.innerHTML = '';

      console.log(`✅ 루트 댓글 ${comments.length}개`);

      comments.forEach(comment => {
        console.log("🔍 렌더링 중인 댓글:", comment);
        const commentNode = renderCommentNode(comment);
        list.appendChild(commentNode);
      });
    })
    .catch(err => {
      console.error('❌ 댓글 불러오기 실패:', err);
    });
}

function renderCommentNode(comment) {
  console.log("🎯 렌더링 중인 댓글:", comment);

  const wrapper = document.createElement('div');
  wrapper.className = 'mb-3';

  const commentHtml = `
    <div class="border-start ps-3 ${comment.parent_id ? 'ms-4' : ''}">
      <strong>${comment.username}</strong>
      <small class="text-muted ms-2">${comment.created_at}</small>
      <p class="mb-1">${comment.comment}</p>
      <button class="btn btn-sm btn-primary mb-2" onclick="showReplyInput(${comment.id})">답글</button>
      <div id="reply-input-${comment.id}" class="mb-2" style="display: none;">
        <textarea class="form-control mb-2" id="reply-comment-${comment.id}" placeholder="대댓글을 입력하세요..."></textarea>
        <button class="btn btn-sm btn-secondary" onclick="submitReply(${comment.id})">대댓글 등록</button>
      </div>
    </div>
  `;

  wrapper.innerHTML = commentHtml;

  // 대댓글 렌더링
  if (comment.replies && comment.replies.length > 0) {
    const repliesContainer = document.createElement('div');
    repliesContainer.className = 'ms-4';

    comment.replies.forEach(reply => {
      const replyNode = renderCommentNode(reply);
      repliesContainer.appendChild(replyNode);
    });

    wrapper.appendChild(repliesContainer);
  }

  return wrapper;
}

function renderCommentNode(comment) {
  console.log("🔍 렌더링 중인 댓글:", comment);
  const wrapper = document.createElement('div');
  wrapper.className = 'mb-3';

  // 댓글 본문
  const commentHtml = `
    <div class="border-start ps-3 ${comment.parent_id ? 'ms-4' : ''}">
      <strong>${comment.username}</strong>
      <small class="text-muted ms-2">${comment.created_at}</small>
      <p class="mb-1">${comment.comment}</p>
      <button class="btn btn-sm bg-white text-brown border-0 fw-bold" onclick="showReplyInput(${comment.id})">⤿ 답글</button>
      <div id="reply-input-${comment.id}" class="mb-2" style="display: none;">
        <textarea class="form-control mb-2" id="reply-comment-${comment.id}" placeholder="입력하세요..."></textarea>
        <button class="btn btn-sm btn-secondary" onclick="submitReply(${comment.id})">답글 등록</button>
      </div>
    </div>
  `;

  wrapper.innerHTML = commentHtml;

  // 대댓글들을 붙일 컨테이너
  const repliesContainer = document.createElement('div');
  repliesContainer.className = 'ms-4';
  repliesContainer.id = `replies-${comment.id}`;

  // 대댓글이 있으면 재귀 호출로 렌더링
  if (comment.replies && comment.replies.length > 0) {
    comment.replies.forEach(reply => {
      repliesContainer.appendChild(renderCommentNode(reply));
    });
  }

  wrapper.appendChild(repliesContainer);
  return wrapper;
}
