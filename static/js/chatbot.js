document.addEventListener('DOMContentLoaded', function () {
  const input = document.getElementById('chat-input');
  const sendButton = document.getElementById('send-button');
  const chatBody = document.getElementById('chat-body');

  // 메시지를 채팅창에 추가하는 함수
  function appendMessage(content, sender) {
    const msg = document.createElement('div');
    msg.className = `chat-message ${sender}`;
  
    if (sender === 'bot') {
      // bot 답변은 마크다운 렌더링
      msg.innerHTML = marked.parse(content);
    } else {
      // 사용자 입력은 텍스트 그대로
      msg.textContent = content;
    }
  
    chatBody.appendChild(msg);
    chatBody.scrollTop = chatBody.scrollHeight;
  }
  
  // 메시지 전송 함수
  async function sendMessage() {
    const userInput = input.value.trim();
    if (!userInput) return;

    appendMessage(userInput, 'user');  // 사용자 입력 먼저 표시
    input.value = '';
    input.disabled = true;
    sendButton.disabled = true;

    try {
      const response = await fetch('http://192.168.219.126:5002/api/ai', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        credentials: 'include', // ✅ 세션 쿠키 포함 필수
        body: JSON.stringify({ prompt: userInput })
      });

      const result = await response.json();

      if (result.status === 'success') {
        let text;

        if (result.data?.candidates) {
          // Gemini API 호출 결과 (비대면진료, 일반 질문)
          text = result.data?.candidates?.[0]?.content?.parts?.[0]?.text || '응답 없음';
        } else {
          // /예약조회 같은 서버 자체 응답
          text = result.data || '응답 없음';
        }

        appendMessage(text, 'bot');
      } else {
        appendMessage(`❗ ${result.message}`, 'bot');
      }

    } catch (error) {
      appendMessage(`❗ 서버 오류 발생: ${error.message}`, 'bot');
    } finally {
      input.disabled = false;
      sendButton.disabled = false;
      input.focus();
    }
  }

  // 버튼 클릭 이벤트
  sendButton.addEventListener('click', sendMessage);

  // 엔터 키 이벤트
  input.addEventListener('keypress', (e) => {
    if (e.key === 'Enter') sendMessage();
  });
});
