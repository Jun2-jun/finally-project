document.addEventListener('DOMContentLoaded', function() {
    const loginForm = document.getElementById('loginForm');
  
    loginForm.addEventListener('submit', function(event) {
      event.preventDefault();
  
      const username = document.getElementById('username').value;
      const password = document.getElementById('password').value;
  
      const loginData = {
        username: username,
        password: password
      };
  
      const apiUrl = 'http://192.168.219.189:5002/api/login';
  
      fetch(apiUrl, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(loginData),
        credentials: 'include',
        mode: 'cors'
      })
      .then(response => {
        const contentType = response.headers.get('content-type');
        if (contentType && contentType.includes('application/json')) {
          return response.json();
        } else {
          throw new Error('응답이 JSON 형식이 아닙니다. 받은 형식: ' + contentType);
        }
      })
      .then(data => {
        if (data.status === 'success') {
          localStorage.setItem('username', data.user);
          window.location.href = '/dashboard';
        } else {
          const errorMessage = document.getElementById('errorMessage');
          errorMessage.textContent = data.message || '로그인에 실패했습니다.';
          errorMessage.style.display = 'block';
        }
      })
      .catch(error => {
        const errorMessage = document.getElementById('errorMessage');
        errorMessage.textContent = '서버 연결 오류: ' + error.message;
        errorMessage.style.display = 'block';
      });
    });
  });
  