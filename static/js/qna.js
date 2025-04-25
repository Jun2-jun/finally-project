// qna.js
document.addEventListener('DOMContentLoaded', function () {
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
  });
  