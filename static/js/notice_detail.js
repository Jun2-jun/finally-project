document.addEventListener('DOMContentLoaded', function () {
    // ✅ 사용자 정보 불러오기
    fetch(`본인 IP:포트/api/current-user`, {
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
    fetch(`본인 IP:포트/api/notices/${postId}`, {
      method: 'GET',
      credentials: 'include',
    })
      .then(res => res.json())
      .then(data => {
        if (data.status === 'success') {
          const post = data.data;
          document.getElementById('post-title').innerText = post.title;
          const postContent = document.getElementById('post-content');
          
          if (Array.isArray(post.image_urls) && post.image_urls.length > 0) {
            const imageContainer = document.createElement('div');
            imageContainer.classList.add('mt-3');
            post.image_urls.forEach(url => {
              const img = document.createElement('img');
              img.src = url;
              img.classList.add('img-thumbnail', 'me-2', 'mb-2');
              img.style.maxWidth = '800px';
              imageContainer.appendChild(img);
            });
            postContent.appendChild(imageContainer);
          }

          const textDiv = document.createElement('div');
          textDiv.innerHTML = post.comment;
          postContent.appendChild(textDiv);
          
        } else {
          document.getElementById('post-content').innerHTML = `<p class="text-danger">공지사항을 불러올 수 없습니다.</p>`;
        }
      })
      .catch(error => {
        console.error('공지사항 상세 불러오기 실패:', error);
        document.getElementById('post-content').innerHTML = `<p class="text-danger">오류가 발생했습니다.</p>`;
      });
  });
  
