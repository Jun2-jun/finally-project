// editor.js

document.addEventListener('DOMContentLoaded', function () {
  const editor = document.getElementById('editor');
  const commentTextarea = document.getElementById('comment');
  const form = document.getElementById('content-form');
  const deleteButton = document.getElementById('toggle-delete');
  const fileUpload = document.getElementById('file-upload');
  const uploadPreview = document.getElementById('upload-preview');
  const insertUpload = document.getElementById('insert-upload');
  const imageUrl = document.getElementById('image-url');
  const urlPreview = document.getElementById('url-preview');
  let selectingMode = false;

  // ========== 글쓰기 페이지: 에디터 기능 ==========
  if (editor && form && commentTextarea) {
    function updatePlaceholder() {
      if (editor.innerHTML.trim() === '' || editor.innerHTML.trim() === '<br>') {
        editor.classList.remove('has-content');
      } else {
        editor.classList.add('has-content');
      }
    }

    updatePlaceholder();

    editor.addEventListener('focus', () => {
      editor.classList.add('focused');
    });

    editor.addEventListener('blur', () => {
      updatePlaceholder();
      editor.classList.remove('focused');
    });

    form.addEventListener('submit', () => {
      commentTextarea.value = editor.innerHTML;
    });

    function exec(cmd, value = null) {
      document.execCommand(cmd, false, value);
      editor.focus();
    }

    const commandButtons = {
      bold: 'bold', italic: 'italic', underline: 'underline', strikethrough: 'strikeThrough',
      'align-left': 'justifyLeft', 'align-center': 'justifyCenter', 'align-right': 'justifyRight', 'align-justify': 'justifyFull',
      'list-ul': 'insertUnorderedList', 'list-ol': 'insertOrderedList', indent: 'indent', outdent: 'outdent', undo: 'undo', redo: 'redo'
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
        editor.innerHTML = '';
        updatePlaceholder();
      }
    });

    // 이미지 관련
    document.getElementById('image')?.addEventListener('click', () => {
      document.getElementById('image-modal').style.display = 'flex';
    });

    document.getElementById('close-modal')?.addEventListener('click', () => {
      document.getElementById('image-modal').style.display = 'none';
      resetImageInputs();
    });

    window.addEventListener('click', (e) => {
      if (e.target === document.getElementById('image-modal')) {
        document.getElementById('image-modal').style.display = 'none';
        resetImageInputs();
      }
    });

    document.querySelectorAll('.tab-button').forEach(btn => {
      btn.addEventListener('click', () => {
        document.querySelectorAll('.tab-button').forEach(b => b.classList.remove('active'));
        document.querySelectorAll('.tab-content').forEach(c => c.classList.remove('active'));
        btn.classList.add('active');
        document.getElementById(`${btn.dataset.tab}-tab`).classList.add('active');
      });
    });

    fileUpload?.addEventListener('change', function () {
      const file = this.files[0];
      if (file && file.type.startsWith('image/')) {
        const reader = new FileReader();
        reader.onload = function (e) {
          uploadPreview.src = e.target.result;
          uploadPreview.style.display = 'block';
          insertUpload.disabled = false;
        };
        reader.readAsDataURL(file);
      }
    });

    imageUrl?.addEventListener('input', function () {
      const url = this.value.trim();
      if (url) {
        urlPreview.src = url;
        urlPreview.style.display = 'block';
      } else {
        urlPreview.style.display = 'none';
      }
    });

    insertUpload?.addEventListener('click', () => {
      insertImage(uploadPreview.src);
      document.getElementById('image-modal').style.display = 'none';
      resetImageInputs();
    });

    document.getElementById('insert-url')?.addEventListener('click', () => {
      const src = imageUrl.value;
      insertImage(src);
      document.getElementById('image-modal').style.display = 'none';
      resetImageInputs();
    });

    function insertImage(src) {
      if (!src) return;
      const img = document.createElement('img');
      img.src = src;
      img.style.maxWidth = '100%';
      img.style.display = 'block';
      img.style.margin = '10px 0';
      editor.appendChild(img);
      updatePlaceholder();
    }

    function resetImageInputs() {
      fileUpload.value = '';
      uploadPreview.src = '';
      uploadPreview.style.display = 'none';
      insertUpload.disabled = true;
      imageUrl.value = '';
      urlPreview.src = '';
      urlPreview.style.display = 'none';
    }
  }

  // ========== 리스트 페이지: 삭제 기능 ==========
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