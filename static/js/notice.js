window.onpageshow = function(event) {
    if (event.persisted) {
        window.location.reload();
    }
};

document.addEventListener('DOMContentLoaded', function () {
    const editor = document.getElementById('editor');
    const commentTextarea = document.getElementById('comment');
    const form = document.getElementById('content-form');
  
    // 에디터 placeholder 설정
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
  
    // 제출 시 에디터 내용을 textarea로 복사
    form?.addEventListener('submit', () => {
      commentTextarea.value = editor.innerHTML;
    });
  
    // execCommand 실행 함수
    function exec(cmd, value = null) {
      document.execCommand(cmd, false, value);
      editor.focus();
    }
  
    // 명령어 버튼 매핑
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
  
    // 폰트 사이즈
    document.getElementById('font-size')?.addEventListener('change', function () {
      exec('fontSize', this.value);
    });
  
    // 폰트 색상
    document.getElementById('font-color')?.addEventListener('input', function () {
      exec('foreColor', this.value);
    });
  
    // 배경 색상
    document.getElementById('bg-color')?.addEventListener('input', function () {
      exec('hiliteColor', this.value);
    });
  
    // 초기화 버튼
    document.getElementById('clear')?.addEventListener('click', () => {
      if (confirm('모든 내용을 지우시겠습니까?')) {
        document.getElementById('title').value = '';
        editor.innerHTML = '내용을 입력하세요';
      }
    });
  
    // 이미지 삽입 기능
    document.getElementById('image')?.addEventListener('click', () => {
      const imageUrl = prompt("이미지 URL을 입력하세요:");
      if (imageUrl) {
        const img = document.createElement('img');
        img.src = imageUrl;
        img.style.maxWidth = '100%';
        img.style.margin = '10px 0';
        editor.appendChild(img);
      }
    });
  });
  