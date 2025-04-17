document.addEventListener('DOMContentLoaded', function () {
  const editor = document.getElementById('editor');
  const commentTextarea = document.getElementById('comment');
  const form = document.getElementById('content-form');

  // Placeholder 처리
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

  // 제출 시 editor 내용 textarea에 복사
  form?.addEventListener('submit', () => {
    commentTextarea.value = editor.innerHTML;
  });

  // 에디터 명령 실행
  function exec(cmd, value = null) {
    document.execCommand(cmd, false, value);
    editor.focus();
  }

  // 버튼 이벤트 매핑
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

  // 이미지 모달 열기
  document.getElementById('image')?.addEventListener('click', () => {
    document.getElementById('image-modal').style.display = 'flex';
  });

  // 모달 닫기
  document.getElementById('close-modal')?.addEventListener('click', () => {
    document.getElementById('image-modal').style.display = 'none';
  });

  // 이미지 삽입 탭 전환
  document.querySelectorAll('.tab-button').forEach(btn => {
    btn.addEventListener('click', () => {
      document.querySelectorAll('.tab-button').forEach(b => b.classList.remove('active'));
      document.querySelectorAll('.tab-content').forEach(c => c.classList.remove('active'));

      btn.classList.add('active');
      const tab = btn.getAttribute('data-tab');
      document.getElementById(`${tab}-tab`).classList.add('active');
    });
  });

  // 업로드 이미지 미리보기
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

  // URL 이미지 미리보기
  document.getElementById('image-url')?.addEventListener('input', function () {
    const preview = document.getElementById('url-preview');
    preview.src = this.value;
    preview.style.display = 'block';
  });

  // 이미지 삽입 - 업로드
  document.getElementById('insert-upload')?.addEventListener('click', () => {
    const src = document.getElementById('upload-preview').src;
    insertImage(src);
    document.getElementById('image-modal').style.display = 'none';
  });

  // 이미지 삽입 - URL
  document.getElementById('insert-url')?.addEventListener('click', () => {
    const src = document.getElementById('image-url').value;
    insertImage(src);
    document.getElementById('image-modal').style.display = 'none';
  });

  // 이미지 삽입 함수
  function insertImage(src) {
    if (!src) return;
    const img = document.createElement('img');
    img.src = src;
    img.style.maxWidth = '100%';
    img.style.display = 'block';
    img.style.margin = '10px 0';
    editor.appendChild(img);
  }
});
