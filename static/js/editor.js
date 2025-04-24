document.addEventListener('DOMContentLoaded', function () {
    const editor = document.getElementById('editor');
    const hiddenTextarea = document.getElementById('comment');
    const form = document.getElementById('content-form');
  
    function isEmptyEditor() {
      return !editor.innerText.trim() || editor.innerHTML === "<br>";
    }
  
    function showPlaceholder() {
      if (isEmptyEditor()) {
        editor.classList.add('placeholder');
        editor.innerText = '내용을 입력하세요';
      }
    }
  
    function hidePlaceholder() {
      if (editor.classList.contains('placeholder')) {
        editor.innerText = '';
        editor.classList.remove('placeholder');
      }
    }
  
    showPlaceholder();
  
    editor.addEventListener('focus', hidePlaceholder);
    editor.addEventListener('blur', showPlaceholder);
  
    form?.addEventListener('submit', function () {
      if (!editor.classList.contains('placeholder')) {
        hiddenTextarea.value = editor.innerHTML;
      } else {
        hiddenTextarea.value = '';
      }
    });
  });
  