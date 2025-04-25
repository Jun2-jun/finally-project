document.addEventListener('DOMContentLoaded', function () {
  // ✅ 삭제 관련 로직
  const deleteButton = document.getElementById('toggle-delete');
  let selectingMode = false;

  if (deleteButton) {
    deleteButton.addEventListener('click', () => {
      const tableBody = document.querySelector('tbody');
      const rows = tableBody?.querySelectorAll('tr');

      if (!selectingMode) {
        rows?.forEach(row => {
          const checkboxCell = row.querySelector('.delete-checkbox-column');
          if (checkboxCell) checkboxCell.style.display = 'table-cell';
        });

        const thead = document.querySelector('thead tr');
        let existing = thead.querySelector('th[data-delete]');
        if (!existing) {
          const th = document.createElement('th');
          th.setAttribute('data-delete', 'true');
          th.classList.add('delete-checkbox-column');
          th.textContent = '선택';
          thead.prepend(th);
        }

        deleteButton.textContent = '삭제 확인';
        selectingMode = true;
      } else {
        const checkedBoxes = document.querySelectorAll('.delete-checkbox:checked');
        if (checkedBoxes.length === 0) {
          alert('삭제할 게시글을 선택하세요.');
          return;
        }

        const deleteIds = Array.from(checkedBoxes).map(box => box.value);

        fetch('/qna/delete', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ delete_ids: deleteIds })
        })
          .then(res => res.json())
          .then(data => {
            if (data.success) {
              checkedBoxes.forEach(box => {
                const row = box.closest('tr');
                row.remove();
              });
              alert('삭제되었습니다.');
            } else {
              alert('삭제 실패: 서버 오류');
            }

            document.querySelectorAll('.delete-checkbox-column').forEach(td => {
              td.style.display = 'none';
            });

            const firstTh = document.querySelector('thead tr th[data-delete]');
            if (firstTh) firstTh.remove();

            deleteButton.textContent = '삭제';
            selectingMode = false;
          })
          .catch(err => {
            alert('삭제 중 오류 발생');
            console.error(err);
          });
      }
    });
  }

  
  // ✅ Q&A 작성 submit 처리
  const form = document.getElementById('content-form');
  if (form) {
    form.addEventListener('submit', function (e) {
      e.preventDefault();

      const title = document.getElementById('title')?.value.trim();
      const comment = document.getElementById('comment')?.value.trim();

      if (!title || !comment) {
        alert('제목과 내용을 모두 입력해주세요.');
        return;
      }

      const formData = new FormData(form);

      fetch('/api/qna', {
        method: 'POST',
        credentials: 'include',
        body: formData
      })
        .then(res => res.json())
        .then(data => {
          if (data.status === 'success') {
            alert('Q&A가 등록되었습니다.');
            window.location.href = '/qna'; // 목록 페이지로 이동
          } else {
            alert(`등록 실패: ${data.message}`);
          }
        })
        .catch(err => {
          alert('등록 중 오류 발생');
          console.error(err);
        });
    });
  }
});
