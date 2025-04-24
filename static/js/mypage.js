document.addEventListener('DOMContentLoaded', () => {
    const editables = document.querySelectorAll('.editable');
    const button = document.getElementById('edit-btn');
    const form = document.getElementById('mypage-form');

    // 🔥 사용자 정보 불러오기
    fetch('http://192.168.219.189:5002/api/current-user', {
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

    // ✏️ 수정 버튼 로직
    button.addEventListener('click', () => {
        const isReadOnly = editables[0].hasAttribute('readonly');

        if (isReadOnly) {
            // 수정 가능하게
            editables.forEach(input => input.removeAttribute('readonly'));
            button.innerText = '수정완료';
        } else {
            // 제출
            form.submit();
        }
    });
});
