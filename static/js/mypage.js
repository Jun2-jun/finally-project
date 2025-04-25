// static/js/mypage.js

document.addEventListener('DOMContentLoaded', () => {
    const editables = document.querySelectorAll('.editable');
    const button = document.getElementById('edit-btn');
    const form = document.getElementById('mypage-form');

    button.addEventListener('click', () => {
        const isReadOnly = editables[0].hasAttribute('readonly');

        if (isReadOnly) {
            // 수정 가능
            editables.forEach(input => input.removeAttribute('readonly'));
            button.innerText = '수정완료';
        } else {
            // 제출
            form.submit();
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