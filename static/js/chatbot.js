document.addEventListener('DOMContentLoaded', function () {
  const input = document.getElementById('chat-input');
  const sendButton = document.getElementById('send-button');
  const chatBody = document.getElementById('chat-body');
  const suggestionContainer = document.getElementById('chat-suggestions');
  
  // 원래 URL을 다시 사용 (하드코딩)
  const API_URL = 'http://172.30.1.39:5002/api/ai';
  
  // 초기 추천 메시지 설정
  const suggestions = [
    { text: '비대면진료', command: '/비대면진료' },
    { text: '예약조회', command: '/예약조회' }
  ];

  // 디버그 모드 - 콘솔에 로그 추가
  const debug = true;
  function log(...args) {
    if (debug) {
      console.log(...args);
    }
  }

  // 추천 버튼 생성
  function createSuggestions() {
    suggestionContainer.innerHTML = '';
    suggestions.forEach(suggestion => {
      const btn = document.createElement('button');
      btn.className = 'suggestion-btn';
      btn.textContent = suggestion.text;
      btn.addEventListener('click', () => {
        input.value = suggestion.command;
        sendMessage();
      });
      suggestionContainer.appendChild(btn);
    });
  }

  // 페이지 로드시 추천 버튼 생성
  createSuggestions();

  // 입력창 클릭 시 추천 버튼 표시
  input.addEventListener('focus', () => {
    suggestionContainer.style.display = 'flex';
  });

  // 메시지를 채팅창에 추가하는 함수
  function appendMessage(content, sender) {
    const msg = document.createElement('div');
    msg.className = `chat-message ${sender}`;
  
    if (sender === 'bot') {
      // bot 답변은 마크다운 렌더링을 시도하되, 오류 시 텍스트로 표시
      try {
        msg.innerHTML = marked.parse(content);
      } catch (e) {
        msg.textContent = content;
        log("마크다운 파싱 오류:", e);
      }
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
    suggestionContainer.style.display = 'none';  // 메시지 전송 시 추천 버튼 숨기기
    
    log("메시지 전송 시작:", userInput);
    
    try {
      // 서버로 전송 (원래 URL 사용)
      log("Fetch 요청:", API_URL);
      const response = await fetch(API_URL, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Accept': 'application/json'
        },
        credentials: 'include', // 세션 쿠키 포함
        body: JSON.stringify({ prompt: userInput })
      });
      
      log("서버 응답 상태:", response.status, response.statusText);
      log("응답 헤더:", [...response.headers.entries()]);
      
      // 직접 응답 내용 확인
      const responseText = await response.text();
      log("응답 내용 전체:", responseText);
      
      // JSON으로 파싱 시도
      let result;
      try {
        result = JSON.parse(responseText);
        log("파싱된 JSON:", result);
      } catch (parseError) {
        log("JSON 파싱 오류:", parseError);
        // JSON 파싱 실패 시, HTML이나 다른 형식일 가능성 있음
        if (responseText.includes("<!DOCTYPE html>") || responseText.includes("<html>")) {
          throw new Error("서버가 HTML 페이지를 반환했습니다. 로그인이 필요하거나 서버 오류가 발생했을 수 있습니다.");
        } else {
          throw new Error("응답을 JSON으로 파싱할 수 없습니다: " + responseText.substring(0, 100) + "...");
        }
      }
      
      if (result.status === 'success') {
        let text;
        if (typeof result.data === 'object' && result.data?.candidates) {
          // Gemini API 호출 결과 (비대면진료, 일반 질문)
          text = result.data?.candidates?.[0]?.content?.parts?.[0]?.text || '응답 없음';
        } else {
          // /예약조회 같은 서버 자체 응답
          text = result.data || '응답 없음';
        }
        appendMessage(text, 'bot');
      } else if (result.status === 'fail') {
        appendMessage(`❗ ${result.message || '오류가 발생했습니다.'}`, 'bot');
      } else {
        appendMessage(`❓ 알 수 없는 응답 형식입니다.`, 'bot');
      }
    } catch (error) {
      log("API 요청 오류:", error);
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

  // 외부 클릭 시 추천 버튼 숨기기
  document.addEventListener('click', (e) => {
    if (!input.contains(e.target) && !suggestionContainer.contains(e.target) && !sendButton.contains(e.target)) {
      suggestionContainer.style.display = 'none';
    }
  });
  
  // 초기 메시지 표시
  log("챗봇 초기화 완료");
});
