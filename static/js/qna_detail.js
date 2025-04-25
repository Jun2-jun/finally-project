// qna_detail.js
document.addEventListener('DOMContentLoaded', function() {
    // 사용자 정보 불러오기
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
            // DOM 요소가 있는지 확인 후 업데이트
            const userNameEl = document.getElementById('user-name');
            const userEmailEl = document.getElementById('user-email');
            
            if (userNameEl) userNameEl.innerText = data.user.username || 'USER';
            if (userEmailEl) userEmailEl.innerText = data.user.email || 'test01@naver.com';
        }
    })
    .catch(err => {
        console.error('사용자 정보 불러오기 실패:', err);
    });
});