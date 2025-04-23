// static/js/dashboard.js

document.addEventListener('DOMContentLoaded', () => {
    fetch('http://localhost:5002/api/current-user', {
      method: 'GET',
      credentials: 'include'
    })
      .then(res => res.json())
      .then(data => {
        if (data.status === 'success') {
          document.getElementById('user-name').innerText = data.user.name || 'USER';
          document.getElementById('user-email').innerText = data.user.email || 'test01@naver.com';
          document.getElementById('welcome-name').innerText = `${data.user.name || 'Test Name'}님!`;
        }
      })
      .catch(err => {
        console.error('사용자 정보 불러오기 실패:', err);
      });
  });
  
  function logout() {
    alert("로그아웃 되었습니다.");
    window.location.href = "/login";
  }
  