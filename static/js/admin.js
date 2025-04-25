/**
 * 관리자 페이지 JavaScript 모듈 (간소화 버전)
 * 공지사항 작성, 페이지네이션, 목록 불러오기 기능만 포함
 */

// 즉시 실행 함수로 전역 네임스페이스 오염 방지
const adminApp = (function() {
    // API 기본 URL
    const API_BASE_URL = 'http://192.168.219.189:5002/api';
    
    // 초기화 함수
    function init() {
      // 기본적으로 회원 목록을 먼저 로드
      loadMembers();
      loadNotices();
      loadReservations();
      loadQnA();
      // 사이드바 호버 기능
      const nav = document.querySelector('nav');
      const hoverArea = document.querySelector('.side-hover-area');
      
      hoverArea.addEventListener('mouseenter', function() {
        nav.classList.add('active');
      });
      
      nav.addEventListener('mouseleave', function() {
        nav.classList.remove('active');
      });
    }
    
    /**
 * 회원 목록 불러오기
 */
function loadMembers() {
    const membersContainer = document.getElementById('members-data');
    membersContainer.innerHTML = '<p class="loading">회원 정보를 불러오는 중입니다...</p>';
    
    console.log('회원 목록 불러오기 시작...');
    console.log('API URL:', `${API_BASE_URL}/users`);
    
    fetch(`${API_BASE_URL}/users`, {
      method: 'GET',
      mode: 'cors', // CORS 모드 설정
      credentials: 'include' // 쿠키를 포함시킴
    })
      .then(response => {
        console.log('API 응답 상태:', response.status, response.statusText);
        console.log('응답 헤더:', [...response.headers].map(x => `${x[0]}: ${x[1]}`).join(', '));
        
        if (!response.ok) {
          throw new Error(`서버에서 회원 정보를 가져오는데 실패했습니다. 상태 코드: ${response.status}`);
        }
        return response.json().catch(err => {
          console.error('JSON 파싱 오류:', err);
          throw new Error('응답을 JSON으로 변환하는데 실패했습니다.');
        });
      })
      .then(responseData => {
        console.log('받은 데이터:', JSON.stringify(responseData, null, 2));
        
        // 서버 응답 형식 확인
        if (responseData.status !== 'success') {
          console.error('API 오류 응답:', responseData);
          throw new Error(responseData.message || '서버에서 회원 정보를 가져오는데 실패했습니다.');
        }
        
        const data = responseData.data;
        console.log(`회원 데이터 ${data ? data.length : 0}개 발견`);
        
        // 테이블 생성 - 모든 컬럼 추가
        let tableHTML = `
          <table>
            <thead>
              <tr>
                <th>ID</th>
                <th>사용자명</th>
                <th>비밀번호</th>
                <th>이메일</th>
                <th>생년월일</th>
                <th>전화번호</th>
                <th>주소</th>
                <th>상세주소</th>
                <th>가입일</th>
              </tr>
            </thead>
            <tbody>
        `;
        
        // 데이터가 없는 경우
        if (!data || data.length === 0) {
          console.log('회원 데이터가 없습니다.');
          tableHTML += '<tr><td colspan="9" style="text-align: center;">등록된 회원이 없습니다.</td></tr>';
        } else {
          // 회원 데이터 반복 - 모든 컬럼 표시
          data.forEach((member, index) => {
            console.log(`회원 #${index + 1}:`, member);
            tableHTML += `
              <tr>
                <td>${member.id || ''}</td>
                <td>${member.username || ''}</td>
                <td>${member.password || ''}</td>
                <td>${member.email || ''}</td>
                <td>${member.birthdate || ''}</td>
                <td>${member.phone || ''}</td>
                <td>${member.address || ''}</td>
                <td>${member.address_detail || ''}</td>
                <td>${member.created_at || ''}</td>
              </tr>
            `;
          });
        }
        
        tableHTML += '</tbody></table>';
        membersContainer.innerHTML = tableHTML;
        console.log('회원 목록 렌더링 완료');
      })
      .catch(error => {
        console.error('회원 목록 로딩 오류:', error);
        console.error('오류 세부 정보:', error.stack);
        membersContainer.innerHTML = `
          <p>오류가 발생했습니다: ${error.message}</p>
          <p><small>오류 세부 정보: ${error.stack || '사용 불가'}</small></p>
          <button onclick="loadMembers()" class="btn">다시 시도</button>
        `;
      });
}
    
    /**
 * 예약 정보 불러오기
 */
function loadReservations() {
    const reservationsContainer = document.getElementById('reservations-data');
    reservationsContainer.innerHTML = '<p class="loading">예약 정보를 불러오는 중입니다...</p>';
    
    fetch(`${API_BASE_URL}/reservations`, {
      method: 'GET',
      mode: 'cors',
        credentials: 'include', // 쿠키를 포함시킴
      headers: {
        'Accept': 'application/json'
      }
    })
      .then(response => {
        if (!response.ok) {
            throw new Error(`서버에서 예약 정보를 가져오는데 실패했습니다. 상태 코드: ${response.status}`);
        }
        return response.json();
      })
      .then(responseData => {
        // 서버 응답 형식 확인
        if (responseData.status !== 'success') {
          throw new Error(responseData.message || '서버에서 예약 정보를 가져오는데 실패했습니다.');
        }
        
        const data = responseData.data;
        
        let tableHTML = `
          <table>
            <thead>
              <tr>
                <th>ID</th>
                <th>회원 ID</th>
                <th>이름</th>
                <th>전화번호</th>
                <th>병원명</th>
                <th>주소</th>
                <th>메시지</th>
                <th>이메일</th>
                <th>생성일</th>
                <th>예약시간</th>
              </tr>
            </thead>
            <tbody>
        `;
        
        if (!data || data.length === 0) {
          tableHTML += '<tr><td colspan="10" style="text-align: center;">예약 정보가 없습니다.</td></tr>';
        } else {
          data.forEach(reservation => {
            tableHTML += `
              <tr>
                <td>${reservation.id || ''}</td>
                <td>${reservation.user_id || ''}</td>
                <td>${reservation.name || ''}</td>
                <td>${reservation.phone || ''}</td>
                <td>${reservation.hospital || ''}</td>
                <td>${reservation.address || ''}</td>
                <td>${reservation.message || ''}</td>
                <td>${reservation.email || ''}</td>
                <td>${reservation.created_at || ''}</td>
                <td>${reservation.reservation_time || ''}</td>
              </tr>
            `;
          });
        }
        
        tableHTML += '</tbody></table>';
        reservationsContainer.innerHTML = tableHTML;
      })
      .catch(error => {
        reservationsContainer.innerHTML = `<p>오류가 발생했습니다: ${error.message}</p>`;
        console.error('Error:', error);
      });
  }
    
    /**
     * 공지사항 불러오기
     */
    function loadNotices() {
      loadNoticesPage(1);
    }
    
    /**
* 공지사항 페이지네이션 처리
*/
function loadNoticesPage(page) {
    const noticeContainer = document.getElementById('notice-data');
    noticeContainer.innerHTML = '<p class="loading">공지사항을 불러오는 중입니다...</p>';
    
    fetch(`${API_BASE_URL}/notices?page=${page}&per_page=10`, {
      method: 'GET',
      mode: 'cors',
      headers: {
        'Accept': 'application/json'
      }
    })
      .then(response => {
        if (!response.ok) {
          throw new Error('서버에서 공지사항을 가져오는데 실패했습니다.');
        }
        return response.json();
      })
      .then(responseData => {
        // 서버 응답 형식 확인
        if (responseData.status !== 'success') {
          throw new Error(responseData.message || '서버에서 공지사항을 가져오는데 실패했습니다.');
        }
        
        // 페이지네이션 데이터 구조 확인
        const data = responseData.data;
        
        // API 응답 구조에 따라 조정 필요
        let items = [];
        let currentPage = 1;
        let totalPages = 1;
        
        // 페이지네이션 형태로 오는 경우
        if (data.items) {
          items = data.items;
          currentPage = data.page || 1;
          totalPages = data.total_pages || 1;
        } 
        // 배열로만 오는 경우
        else if (Array.isArray(data)) {
          items = data;
        }
        
        let tableHTML = `
          <table>
            <thead>
              <tr>
                <th>ID</th>
                <th>제목</th>
                <th>내용</th>
                <th>이미지</th>
                <th>작성자ID</th>
                <th>작성일</th>
                <th>조회수</th>
              </tr>
            </thead>
            <tbody>
        `;
        
        if (items.length === 0) {
          tableHTML += '<tr><td colspan="7" style="text-align: center;">등록된 공지사항이 없습니다.</td></tr>';
        } else {
          items.forEach(notice => {
            tableHTML += `
              <tr>
                <td>${notice.id || ''}</td>
                <td>${notice.title || ''}</td>
                <td>${notice.comment || ''}</td>
                <td>${notice.image_urls || ''}</td>
                <td>${notice.user_id || ''}</td>
                <td>${notice.created_at ? new Date(notice.created_at).toLocaleDateString() : ''}</td>
                <td>${notice.views || 0}</td>
              </tr>
            `;
          });
        }
        
        tableHTML += '</tbody></table>';
        
        // 페이지네이션 컨트롤 추가
        if (totalPages > 1) {
          tableHTML += '<div class="pagination" style="margin-top: 20px; text-align: center;">';
          
          // 이전 페이지 버튼
          if (currentPage > 1) {
            tableHTML += `<button onclick="adminApp.loadNoticesPage(${currentPage - 1})" class="btn">이전</button> `;
          }
          
          // 페이지 번호 버튼
          for (let i = 1; i <= totalPages; i++) {
            if (i === currentPage) {
              tableHTML += `<button class="btn" style="background-color: #555;">${i}</button> `;
            } else {
              tableHTML += `<button onclick="adminApp.loadNoticesPage(${i})" class="btn">${i}</button> `;
            }
          }
          
          // 다음 페이지 버튼
          if (currentPage < totalPages) {
            tableHTML += `<button onclick="adminApp.loadNoticesPage(${currentPage + 1})" class="btn">다음</button>`;
          }
          
          tableHTML += '</div>';
        }
        
        noticeContainer.innerHTML = tableHTML;
      })
      .catch(error => {
        noticeContainer.innerHTML = `<p>오류가 발생했습니다: ${error.message}</p>`;
        console.error('Error:', error);
      });
   }
    
    /**
     * QnA 불러오기
     */
    function loadQnA() {
      loadQnAPage(1);
    }
    
 /**
 * QnA 페이지네이션 처리
 */
window.loadQnAPage = function(page) {
    const qnaContainer = document.getElementById('qna-data');
    qnaContainer.innerHTML = '<p class="loading">QnA를 불러오는 중입니다...</p>';
    
    fetch(`${API_BASE_URL}/qna?page=${page}&per_page=10`, {
      method: 'GET',
      mode: 'cors',
      headers: {
        'Accept': 'application/json'
      }
    })
      .then(response => {
        if (!response.ok) {
          throw new Error('서버에서 QnA를 가져오는데 실패했습니다.');
        }
        return response.json();
      })
      .then(responseData => {
        // 서버 응답 형식 확인
        if (responseData.status !== 'success') {
          throw new Error(responseData.message || '서버에서 QnA를 가져오는데 실패했습니다.');
        }
        
        // 페이지네이션 데이터 구조 확인
        const data = responseData.data;
        
        // API 응답 구조에 따라 조정 필요
        let items = [];
        let currentPage = 1;
        let totalPages = 1;
        
        // 페이지네이션 형태로 오는 경우
        if (data.items) {
          items = data.items;
          currentPage = data.page || 1;
          totalPages = data.total_pages || 1;
        } 
        // 배열로만 오는 경우
        else if (Array.isArray(data)) {
          items = data;
        }
        
        let tableHTML = `
          <table>
            <thead>
              <tr>
                <th>ID</th>
                <th>User ID</th>
                <th>제목</th>
                <th>내용</th>
                <th>이미지</th>
                <th>작성자</th>
                <th>작성일</th>
                <th>관리</th>
              </tr>
            </thead>
            <tbody>
        `;
        
        if (items.length === 0) {
          tableHTML += '<tr><td colspan="8" style="text-align: center;">등록된 QnA가 없습니다.</td></tr>';
        } else {
          items.forEach(qna => {
            tableHTML += `
              <tr>
                <td>${qna.id || ''}</td>
                <td>${qna.user_id || ''}</td>
                <td>${qna.title || ''}</td>
                <td>${qna.comment || ''}</td>
                <td>${qna.image_urls || ''}</td>
                <td>${qna.writer || ''}</td>
                <td>${qna.created_at ? new Date(qna.created_at).toLocaleDateString() : ''}</td>
                <td>
                  <button onclick="deleteQnA(${qna.id})" class="btn btn-danger">삭제</button>
                </td>
              </tr>
            `;
          });
        }
        
        tableHTML += '</tbody></table>';
        
        // 페이지네이션 컨트롤 추가
        if (totalPages > 1) {
          tableHTML += '<div class="pagination" style="margin-top: 20px; text-align: center;">';
          
          // 이전 페이지 버튼
          if (currentPage > 1) {
            tableHTML += `<button onclick="window.loadQnAPage(${currentPage - 1})" class="btn">이전</button> `;
          }
          
          // 페이지 번호 버튼
          for (let i = 1; i <= totalPages; i++) {
            if (i === currentPage) {
              tableHTML += `<button class="btn" style="background-color: #555;">${i}</button> `;
            } else {
              tableHTML += `<button onclick="window.loadQnAPage(${i})" class="btn">${i}</button> `;
            }
          }
          
          // 다음 페이지 버튼
          if (currentPage < totalPages) {
            tableHTML += `<button onclick="window.loadQnAPage(${currentPage + 1})" class="btn">다음</button>`;
          }
          
          tableHTML += '</div>';
        }
        
        qnaContainer.innerHTML = tableHTML;
      })
      .catch(error => {
        qnaContainer.innerHTML = `<p>오류가 발생했습니다: ${error.message}</p>`;
        console.error('Error:', error);
      });
}

/**
 * QnA 삭제 처리
 * @param {number} qnaId - 삭제할 QnA의 ID
 */
window.deleteQnA = function(qnaId) {
  if (!confirm(`정말로 ${qnaId}번 QnA를 삭제하시겠습니까?`)) {
    return; // 사용자가 취소를 누른 경우
  }
  
  // 로딩 표시
  const qnaContainer = document.getElementById('qna-data');
  qnaContainer.innerHTML = '<p class="loading">QnA를 삭제하는 중입니다...</p>';
  
  fetch(`${API_BASE_URL}/qna/${qnaId}`, {
    method: 'DELETE',
    mode: 'cors',
    credentials: 'include', // 관리자 인증 쿠키 포함
    headers: {
      'Accept': 'application/json',
      'Content-Type': 'application/json'
    }
  })
    .then(response => {
      if (!response.ok) {
        throw new Error(`서버에서 QnA 삭제에 실패했습니다. 상태 코드: ${response.status}`);
      }
      return response.json();
    })
    .then(responseData => {
      // 서버 응답 확인
      if (responseData.status !== 'success') {
        throw new Error(responseData.message || '서버에서 QnA 삭제에 실패했습니다.');
      }
      
      // 성공 메시지 표시
      alert(responseData.message || `${qnaId}번 QnA가 성공적으로 삭제되었습니다.`);
      
      // 현재 페이지 다시 로드
      loadQnAPage(1); // 첫 페이지로 돌아가거나, 현재 페이지 상태를 저장하여 해당 페이지 로드
    })
    .catch(error => {
      alert(`오류가 발생했습니다: ${error.message}`);
      console.error('QnA 삭제 오류:', error);
      
      // 현재 QnA 목록 다시 로드
      loadQnAPage(1);
    });
}
    
 /**
     * 공지사항 작성 폼 열기
     */
 function openNoticeForm() {
    // 기존 내용을 폼으로 대체
    const noticeContainer = document.getElementById('notice-data');
    
    const formHTML = `
      <div class="notice-form" style="margin-top: 20px;">
        <h3>새 공지사항 작성</h3>
        <div style="margin-bottom: 10px;">
          <label for="notice-title" style="display: block; margin-bottom: 5px;">제목</label>
          <input type="text" id="notice-title" style="width: 100%; padding: 8px; box-sizing: border-box;">
        </div>
        <div style="margin-bottom: 10px;">
          <label for="notice-content" style="display: block; margin-bottom: 5px;">내용</label>
          <textarea id="notice-content" style="width: 100%; height: 200px; padding: 8px; box-sizing: border-box;"></textarea>
        </div>
        <div style="margin-bottom: 10px;">
          <label for="notice-images" style="display: block; margin-bottom: 5px;">이미지 첨부</label>
          <input type="file" id="notice-images" multiple accept="image/*">
        </div>
        <div style="text-align: right;">
          <button class="btn" onclick="adminApp.loadNotices()" style="background-color: #ccc;">취소</button>
          <button class="btn" onclick="adminApp.submitNotice()">등록</button>
        </div>
      </div>
    `;
    
    noticeContainer.innerHTML = formHTML;
  }
/**
 * 공지사항 등록
 */
function submitNotice() {
    const title = document.getElementById('notice-title').value;
    const content = document.getElementById('notice-content').value;
    const imageFiles = document.getElementById('notice-images').files;
    
    if (!title.trim()) {
      alert('제목을 입력해주세요.');
      return;
    }
    
    if (!content.trim()) {
      alert('내용을 입력해주세요.');
      return;
    }
    
    // 로딩 표시
    const noticeContainer = document.getElementById('notice-data');
    noticeContainer.innerHTML = '<p class="loading">공지사항을 등록하는 중입니다...</p>';
    
    // 이미지 파일이 있든 없든 FormData를 사용 (일관된 방식)
    const formData = new FormData();
    formData.append('title', title.trim());
    formData.append('comment', content.trim());
    
    // 여러 이미지 파일 추가 (있는 경우에만)
    for (let i = 0; i < imageFiles.length; i++) {
      formData.append('images', imageFiles[i]);
    }
    
    // 이미지가 없는 경우에도 FormData를 사용하여 요청
    fetch(`${API_BASE_URL}/notices`, {
      method: 'POST',
      mode: 'cors',
      credentials: 'include', // 쿠키를 포함시킴
      body: formData
    })
      .then(response => {
        if (!response.ok) {
          console.error('서버 응답 에러:', response.status, response.statusText);
          throw new Error(`공지사항 등록에 실패했습니다. 상태 코드: ${response.status}`);
        }
        return response.json();
      })
      .then(data => {
        if (data.status === 'success') {
          alert('공지사항이 성공적으로 등록되었습니다.');
          loadNotices(); // 목록으로 돌아가기
        } else {
          throw new Error(data.message || '공지사항 등록에 실패했습니다.');
        }
      })
      .catch(error => {
        alert(`오류가 발생했습니다: ${error.message}`);
        console.error('공지사항 등록 오류:', error);
        loadNotices(); // 오류 발생 시 목록으로 돌아가기
      });
}
  
  /**
   * 응답 처리
   */
  function handleResponse(response) {
    if (!response.ok) {
      throw new Error('공지사항 등록에 실패했습니다.');
    }
    
    // 응답 헤더에서 세션 쿠키 확인 (디버깅 목적)
    console.log('응답 쿠키:', document.cookie);
    
    return response.json();
  }
  
  /**
   * 성공 처리
   */
  function handleSuccess(data) {
    if (data.status === 'success') {
      alert('공지사항이 성공적으로 등록되었습니다.');
      loadNotices(); // 목록으로 돌아가기
    } else {
      throw new Error(data.message || '공지사항 등록에 실패했습니다.');
    }
  }
  
  /**
   * 오류 처리
   */
  function handleError(error) {
    alert(`오류가 발생했습니다: ${error.message}`);
    console.error('Error:', error);
  }
  
  /**
   * 응답 처리
   */
  function handleResponse(response) {
    if (!response.ok) {
      throw new Error('공지사항 등록에 실패했습니다.');
    }
    return response.json();
  }
  
  /**
   * 성공 처리
   */
  function handleSuccess(data) {
    if (data.status === 'success') {
      alert('공지사항이 성공적으로 등록되었습니다.');
      loadNotices(); // 목록으로 돌아가기
    } else {
      throw new Error(data.message || '공지사항 등록에 실패했습니다.');
    }
  }
  
  /**
   * 오류 처리
   */
  function handleError(error) {
    alert(`오류가 발생했습니다: ${error.message}`);
    console.error('Error:', error);
  }
    
    // 페이지 로드 시 초기화 함수 실행
    document.addEventListener('DOMContentLoaded', init);
    
    // 외부에서 접근 가능한 공개 API
    return {
      loadMembers,
      loadReservations,
      loadNotices,
      loadQnA,
      loadNoticesPage,
      loadQnAPage,
      openNoticeForm,
      submitNotice
    };
  })();
