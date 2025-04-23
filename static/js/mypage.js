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
