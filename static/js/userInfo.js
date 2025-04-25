document.addEventListener('DOMContentLoaded', () => {
    console.log("👤 [userinfo.js] 사용자 정보 가져오기 시작");
  
    fetch('http://192.168.219.189:5002/api/current-user', {
      method: 'GET',
      credentials: 'include'
    })
      .then(res => res.json())
      .then(data => {
        if (data.status === 'success') {
          const username = data.user.username || 'USER';
          const email = data.user.email || 'test01@naver.com';
  
          // 사이드바
          const userNameEl = document.getElementById('user-name');
          const userEmailEl = document.getElementById('user-email');
  
          // 대시보드 배너
          const welcomeNameEl = document.getElementById('welcome-name');
  
          if (userNameEl) userNameEl.innerText = username;
          if (userEmailEl) userEmailEl.innerText = email;
          if (welcomeNameEl) welcomeNameEl.innerText = `${username}님!`;
        }
      })
      .catch(err => {
        console.error('❌ [userinfo.js] 사용자 정보 로딩 실패:', err);
      });
  });
  
  function logout() {
    fetch('/logout', {
      method: 'POST', // or GET depending on your server route
      credentials: 'include'
    })
    .then(res => {
      alert("로그아웃 되었습니다.");
      window.location.href = "/login";
    });
  }
