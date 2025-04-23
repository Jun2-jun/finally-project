// chatbot.js
document.addEventListener('DOMContentLoaded', function () {
    const input = document.getElementById('chat-input');
    const sendButton = document.getElementById('send-button');
    const chatBody = document.getElementById('chat-body');
  
    function appendMessage(content, sender) {
      const msg = document.createElement('div');
      msg.className = `chat-message ${sender}`;
      msg.textContent = content;
      chatBody.appendChild(msg);
      chatBody.scrollTop = chatBody.scrollHeight;
    }
  
    function sendMessage() {
      const userInput = input.value.trim();
      if (!userInput) return;
      appendMessage(userInput, 'user');
      input.value = '';
  
      // 실제 HuggingFace API 호출은 여기서 처리해야 함
      setTimeout(() => {
        appendMessage('이건 예시 응답입니다. 나중에 모델 연동해주세요.', 'bot');
      }, 1000);
    }
  
    sendButton.addEventListener('click', sendMessage);
    input.addEventListener('keypress', (e) => {
      if (e.key === 'Enter') sendMessage();
    });
  });
  