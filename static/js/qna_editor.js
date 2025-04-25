// editor.js

document.addEventListener('DOMContentLoaded', function () {
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
        const welcomeNameEl = document.getElementById('welcome-name');
        
        if (userNameEl) userNameEl.innerText = data.user.username || 'USER';
        if (userEmailEl) userEmailEl.innerText = data.user.email || 'test01@naver.com';
        if (welcomeNameEl) welcomeNameEl.innerText = `${data.user.username || 'Test Name'}님!`;
      }
    })
    .catch(err => {
      console.error('사용자 정보 불러오기 실패:', err);
    });

  // 기존 에디터 기능
  const editor = document.getElementById('editor');
  const commentTextarea = document.getElementById('comment');
  const form = document.getElementById('content-form');
  const deleteButton = document.getElementById('toggle-delete');
  const fileUpload = document.getElementById('file-upload');
  const uploadPreview = document.getElementById('upload-preview');
  const insertUpload = document.getElementById('insert-upload');
  const imageUrl = document.getElementById('image-url');
  const urlPreview = document.getElementById('url-preview');
  const uploadedFilesContainer = document.getElementById('uploaded-images');
  const imageCountText = document.getElementById('image-count');
  let selectingMode = false;
  let uploadCount = 0;

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
        uploadedFilesContainer.innerHTML = '';
        uploadCount = 0;
        updateUploadCount(0, true);
        updatePlaceholder();
      }
    });

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
          insertImage(e.target.result);
          addUploadedFile(file.name, e.target.result);
          document.getElementById('image-modal').style.display = 'none';
          resetImageInputs();
        };
        reader.readAsDataURL(file);
      }
    });

    imageUrl?.addEventListener('input', function () {
      const url = this.value.trim();
      urlPreview.src = url;
      urlPreview.style.display = url ? 'block' : 'none';
    });

    insertUpload?.addEventListener('click', () => {
      if (uploadPreview.src) {
        insertImage(uploadPreview.src);
        addUploadedFile('업로드 이미지', uploadPreview.src);
        document.getElementById('image-modal').style.display = 'none';
        resetImageInputs();
      }
    });

    document.getElementById('insert-url')?.addEventListener('click', () => {
      const src = imageUrl.value;
      insertImage(src);
      addUploadedFile(src, src);
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

    function addUploadedFile(filename, src = null) {
      if (!uploadedFilesContainer || !imageCountText) return;

      const fileItem = document.createElement('div');
      fileItem.classList.add('file-item');

      fileItem.innerHTML = `
        <span class="file-name">${filename}</span>
        <button type="button" class="remove-btn" title="삭제">&times;</button>
      `;

      fileItem.querySelector('.remove-btn').addEventListener('click', () => {
        uploadedFilesContainer.removeChild(fileItem);
        updateUploadCount(-1);

        if (src) {
          const images = editor.querySelectorAll('img');
          images.forEach(img => {
            if (img.src === src) {
              img.remove();
            }
          });
        }
      });

      uploadedFilesContainer.appendChild(fileItem);
      updateUploadCount(1);
    }

    function updateUploadCount(delta, reset = false) {
      uploadCount = reset ? 0 : uploadCount + delta;
      imageCountText.textContent = uploadCount;
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
});