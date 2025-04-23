document.addEventListener('DOMContentLoaded', () => {
    fetch('http://192.168.219.62:5002/api/current-user', {
      method: 'GET',
      credentials: 'include'
    })
      .then(res => res.json())
      .then(data => {
        if (data.status === 'success') {
          document.getElementById('user-name').innerText = data.user.username || 'USER';  // ✅ 수정
          document.getElementById('user-email').innerText = data.user.email || 'test01@naver.com';
          document.getElementById('welcome-name').innerText = `${data.user.username || 'Test Name'}님!`;  // ✅ 수정
        }
      })
      .catch(err => {
        console.error('사용자 정보 불러오기 실패:', err);
      });
});
