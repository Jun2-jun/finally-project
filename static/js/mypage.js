document.addEventListener('DOMContentLoaded', () => {
    const editables = document.querySelectorAll('.editable');
    const button = document.getElementById('edit-btn');
    const form = document.getElementById('mypage-form');

    // 🔥 1. 사용자 정보 불러오기
    fetch('http://192.168.219.126:5002/api/current-user', {
        method: 'GET',
        credentials: 'include'
    })
    .then(res => res.json())
    .then(data => {
        if (data.status === 'success') {
            const user = data.user;
            document.querySelector('[name="userid"]').value = user.username || '';
            document.querySelector('[name="email"]').value = user.email || '';
            document.querySelector('[name="birthdate"]').value = user.birthdate || '';
            document.querySelector('[name="phone"]').value = user.phone || '';
            document.querySelector('[name="address"]').value = user.address || '';
            document.querySelector('[name="detail_address"]').value = user.address_detail || '';
        } else {
            console.error('유저 정보 로딩 실패:', data.message);
        }
    })
    .catch(error => {
        console.error('API 호출 실패:', error);
    });

    // ✅ 2. 수정 버튼 동작 처리
    button.addEventListener('click', async () => {
        const isReadOnly = editables[0].hasAttribute('readonly');

        if (isReadOnly) {
            // 입력 가능 상태로 전환
            editables.forEach(input => input.removeAttribute('readonly'));
            button.innerText = '수정완료';
        } else {
            // 수정 완료 → 서버에 정보 업데이트
            const email = document.querySelector('[name="email"]').value;
            const birthdate = document.querySelector('[name="birthdate"]').value;
            const phone = document.querySelector('[name="phone"]').value;
            const address = document.querySelector('[name="address"]').value;
            const detail_address = document.querySelector('[name="detail_address"]').value;

            try {
                const response = await fetch('http://192.168.219.126:5002/api/users/update', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    credentials: 'include',
                    body: JSON.stringify({
                        email,
                        birthdate,
                        phone,
                        address,
                        address_detail: detail_address
                    })
                });

                const result = await response.json();

                if (result.status === 'success') {
                    alert('정보가 성공적으로 수정되었습니다.');
                    editables.forEach(input => input.setAttribute('readonly', true));
                    button.innerText = '수정하기';
                } else {
                    alert(`수정 실패: ${result.message}`);
                }
            } catch (err) {
                alert('서버 요청 중 오류가 발생했습니다.');
                console.error(err);
            }
        }
    });
});

function submitWithdraw() {
    const password = document.getElementById('withdrawPassword').value;
    const errorText = document.getElementById('withdrawError');
  
    if (!password) {
      alert('비밀번호를 입력해주세요.');
      return;
    }
  
    fetch("/confirm_delete", {
      method: "POST",
      headers: {
        "Content-Type": "application/x-www-form-urlencoded"
      },
      body: new URLSearchParams({ password })
    })
    .then(response => {
      if (response.redirected) {
        window.location.href = response.url;
      } else {
        errorText.style.display = 'block';
      }
    })
    .catch(() => {
      errorText.style.display = 'block';
    });
  }

  function submitWithdraw() {
    const password = document.getElementById('withdrawPassword').value;
    const errorMsg = document.getElementById('withdrawError');
  
    fetch('/api/users/check-password', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ password: password })
    })
    .then(res => res.json())
    .then(data => {
      if (data.success) {
        errorMsg.style.display = 'none';
  
        // 실제 탈퇴 요청
        fetch('/api/users/withdraw', {
          method: 'POST'
        }).then(() => {
          document.querySelector('.modal-body').style.display = 'none';
          document.getElementById('withdrawSuccess').style.display = 'block';
        });
      } else {
        errorMsg.textContent = data.message || '비밀번호가 일치하지 않습니다.';
        errorMsg.style.display = 'block';
      }
    })
    .catch(err => {
      console.error('에러:', err);
      errorMsg.textContent = '서버 오류가 발생했습니다.';
      errorMsg.style.display = 'block';
    });
  }
