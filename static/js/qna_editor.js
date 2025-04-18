document.addEventListener('DOMContentLoaded', function () {
  const editor = document.getElementById('editor');
  const commentTextarea = document.getElementById('comment');
  const form = document.getElementById('content-form');
  const deleteButton = document.getElementById('toggle-delete');
  let selectingMode = false;

  /** =============================
   * 글쓰기 페이지: 에디터 기능
   * ============================= */
  if (editor && form && commentTextarea) {
    function updatePlaceholder() {
      if (editor.textContent.trim() === '') {
        editor.textContent = '내용을 입력하세요';
        editor.classList.add('placeholder');
      }
    }

    updatePlaceholder();

    editor.addEventListener('focus', () => {
      if (editor.classList.contains('placeholder')) {
        editor.textContent = '';
        editor.classList.remove('placeholder');
      }
    });

    editor.addEventListener('blur', updatePlaceholder);

    form.addEventListener('submit', () => {
      commentTextarea.value = editor.innerHTML;
    });

    function exec(cmd, value = null) {
      document.execCommand(cmd, false, value);
      editor.focus();
    }

    const commandButtons = {
      bold: 'bold',
      italic: 'italic',
      underline: 'underline',
      strikethrough: 'strikeThrough',
      'align-left': 'justifyLeft',
      'align-center': 'justifyCenter',
      'align-right': 'justifyRight',
      'align-justify': 'justifyFull',
      'list-ul': 'insertUnorderedList',
      'list-ol': 'insertOrderedList',
      indent: 'indent',
      outdent: 'outdent',
      undo: 'undo',
      redo: 'redo'
    };

    Object.entries(commandButtons).forEach(([id, command]) => {
      document.getElementById(id)?.addEventListener('click', () => exec(command));
    });

    document.getElementById('font-size')?.addEventListener('change', function () {
      exec('fontSize', this.value);
    });

    document.getElementById('font-color')?.addEventListener('input', function () {
      exec('foreColor', this.value);
    });

    document.getElementById('bg-color')?.addEventListener('input', function () {
      exec('hiliteColor', this.value);
    });

    document.getElementById('clear')?.addEventListener('click', () => {
      if (confirm('모든 내용을 지우시겠습니까?')) {
        document.getElementById('title').value = '';
        editor.innerHTML = '내용을 입력하세요';
      }
    });

    // 이미지 관련
    document.getElementById('image')?.addEventListener('click', () => {
      document.getElementById('image-modal').style.display = 'flex';
    });

    document.getElementById('close-modal')?.addEventListener('click', () => {
      document.getElementById('image-modal').style.display = 'none';
    });

    document.querySelectorAll('.tab-button').forEach(btn => {
      btn.addEventListener('click', () => {
        document.querySelectorAll('.tab-button').forEach(b => b.classList.remove('active'));
        document.querySelectorAll('.tab-content').forEach(c => c.classList.remove('active'));

        btn.classList.add('active');
        const tab = btn.getAttribute('data-tab');
        document.getElementById(`${tab}-tab`).classList.add('active');
      });
    });

    document.getElementById('file-upload')?.addEventListener('change', function () {
      const file = this.files[0];
      if (!file) return;
      const reader = new FileReader();
      reader.onload = () => {
        const preview = document.getElementById('upload-preview');
        preview.src = reader.result;
        preview.style.display = 'block';
      };
      reader.readAsDataURL(file);
    });

    document.getElementById('image-url')?.addEventListener('input', function () {
      const preview = document.getElementById('url-preview');
      preview.src = this.value;
      preview.style.display = 'block';
    });

    document.getElementById('insert-upload')?.addEventListener('click', () => {
      const src = document.getElementById('upload-preview').src;
      insertImage(src);
      document.getElementById('image-modal').style.display = 'none';
    });

    document.getElementById('insert-url')?.addEventListener('click', () => {
      const src = document.getElementById('image-url').value;
      insertImage(src);
      document.getElementById('image-modal').style.display = 'none';
    });

    function insertImage(src) {
      if (!src) return;
      const img = document.createElement('img');
      img.src = src;
      img.style.maxWidth = '100%';
      img.style.display = 'block';
      img.style.margin = '10px 0';
      editor.appendChild(img);
    }
  }


  /** =============================
 * 리스트 페이지: 삭제 기능
 * ============================= */
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
      const existing = thead.querySelector('th[data-delete]');
      if (!existing) {
        const th = document.createElement('th');
        th.setAttribute('data-delete', 'true');
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

      // 서버에 삭제 요청 보내기
      fetch('/qna/delete', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({ delete_ids: deleteIds })
      })
        .then(res => res.json())
        .then(data => {
          if (data.success) {
            // UI에서 제거
            checkedBoxes.forEach(box => {
              const row = box.closest('tr');
              row.remove();
            });

            alert('삭제되었습니다.');
          } else {
            alert('삭제 실패: 서버 오류');
          }

          // UI 정리
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
