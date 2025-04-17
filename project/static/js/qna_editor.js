document.addEventListener('DOMContentLoaded', function () {
    const editor = document.getElementById('editor');
    const commentTextarea = document.getElementById('comment');
    const form = document.getElementById('content-form');
  
    // placeholder 처리
    if (editor.textContent.trim() === '' || editor.textContent === '내용을 입력하세요') {
      editor.textContent = '내용을 입력하세요';
      editor.classList.add('placeholder');
    }
  
    editor.addEventListener('focus', function () {
      if (editor.classList.contains('placeholder')) {
        editor.textContent = '';
        editor.classList.remove('placeholder');
      }
    });
  
    editor.addEventListener('blur', function () {
      if (editor.textContent.trim() === '') {
        editor.textContent = '내용을 입력하세요';
        editor.classList.add('placeholder');
      }
    });
  
    // 폼 제출 시 editor 내용을 textarea에 복사
    form.addEventListener('submit', function () {
      commentTextarea.value = editor.innerHTML;
    });
  
    // 툴바 버튼 동작
    function exec(cmd, value = null) {
      document.execCommand(cmd, false, value);
      editor.focus();
    }
  
    document.getElementById('bold')?.addEventListener('click', () => exec('bold'));
    document.getElementById('italic')?.addEventListener('click', () => exec('italic'));
    document.getElementById('underline')?.addEventListener('click', () => exec('underline'));
    document.getElementById('strikethrough')?.addEventListener('click', () => exec('strikeThrough'));
  
    document.getElementById('align-left')?.addEventListener('click', () => exec('justifyLeft'));
    document.getElementById('align-center')?.addEventListener('click', () => exec('justifyCenter'));
    document.getElementById('align-right')?.addEventListener('click', () => exec('justifyRight'));
    document.getElementById('align-justify')?.addEventListener('click', () => exec('justifyFull'));
  
    document.getElementById('list-ul')?.addEventListener('click', () => exec('insertUnorderedList'));
    document.getElementById('list-ol')?.addEventListener('click', () => exec('insertOrderedList'));
    document.getElementById('indent')?.addEventListener('click', () => exec('indent'));
    document.getElementById('outdent')?.addEventListener('click', () => exec('outdent'));
  
    document.getElementById('font-size')?.addEventListener('change', function () {
      exec('fontSize', this.value);
    });
  
    document.getElementById('font-color')?.addEventListener('input', function () {
      exec('foreColor', this.value);
    });
  
    document.getElementById('bg-color')?.addEventListener('input', function () {
      exec('hiliteColor', this.value);
    });
  
    document.getElementById('undo')?.addEventListener('click', () => exec('undo'));
    document.getElementById('redo')?.addEventListener('click', () => exec('redo'));
  
    document.getElementById('clear')?.addEventListener('click', () => {
      if (confirm('모든 내용을 지우시겠습니까?')) {
        document.getElementById('title').value = '';
        editor.innerHTML = '내용을 입력하세요';
      }
    });
  });
  