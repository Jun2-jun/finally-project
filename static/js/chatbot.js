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

  async function sendMessage() {
    const userInput = input.value.trim();
    if (!userInput) return;

    appendMessage(userInput, 'user');
    input.value = '';

    try {
      const response = await fetch('http://192.168.219.189:5002/api/ai', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          prompt: userInput
        })
      });

      const result = await response.json();

      if (result.status === 'success') {
        appendMessage(result.data.response || '응답 없음', 'bot');
      } else {
        appendMessage(`❗ ${result.message}`, 'bot');
      }
    } catch (error) {
      appendMessage(`❗ 서버 오류 발생: ${error.message}`, 'bot');
    }
  }

  sendButton.addEventListener('click', sendMessage);
  input.addEventListener('keypress', (e) => {
    if (e.key === 'Enter') sendMessage();
  });
});
