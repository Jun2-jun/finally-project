document.addEventListener('DOMContentLoaded', function () {
  const tbody = document.getElementById('qnaTableBody');
  const pagination = document.getElementById('pagination');
  const deleteButton = document.getElementById('toggle-delete');
  const form = document.getElementById('content-form');
  const searchButton = document.getElementById('search-button');
  const searchInput = document.getElementById('search-input');
  const welcomeNameEl = document.getElementById('welcome-name');
  const userNameEl = document.getElementById('user-name');
  const userEmailEl = document.getElementById('user-email');
  const serverIP = document.body.dataset.serverIp;
  
  let selectingMode = false;
  let currentPage = 1;
  let currentKeyword = "";

  // ✅ 사용자 정보 불러오기
  fetch(`http://${serverIP}:5002/api/current-user`, {
    method: 'GET',
    credentials: 'include'
  })
  .then(res => res.json())
  .then(data => {
    if (data.status === 'success') {
      const username = data.user.username || 'USER';
      const email = data.user.email || 'test01@naver.com';
      if (userNameEl) userNameEl.innerText = username;
      if (userEmailEl) userEmailEl.innerText = email;
      if (welcomeNameEl) welcomeNameEl.innerText = `${username}님!`;
    }
  })
  .catch(err => {
    console.error('❌ 사용자 정보 로딩 실패:', err);
  });

  // ✅ 삭제 버튼 클릭
  if (deleteButton) {
    deleteButton.addEventListener('click', () => {
      const tableBody = document.querySelector('tbody');
      const rows = tableBody?.querySelectorAll('tr');

      if (!selectingMode) {
        rows?.forEach(row => {
          const checkboxCell = row.querySelector('.delete-checkbox-column');
          if (checkboxCell) checkboxCell.style.display = 'table-cell';
        });

        const thead = document.querySelector('thead tr');
        let existing = thead.querySelector('th[data-delete]');
        if (!existing) {
          const th = document.createElement('th');
          th.setAttribute('data-delete', 'true');
          th.classList.add('delete-checkbox-column');
          th.textContent = '선택';
          thead.prepend(th);
        }

        deleteButton.textContent = '삭제 확인';
        selectingMode = true;
      } else {
        const checkedBoxes = document.querySelectorAll('.delete-checkbox:checked');
        if (checkedBoxes.length === 0) {
          alert('삭제할 게시글을 선택하세요.');
          return;
        }

        const deleteIds = Array.from(checkedBoxes).map(box => box.value);

        fetch(`http://${serverIP}:5002/qna/delete`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ delete_ids: deleteIds })
        })
        .then(res => res.json())
        .then(data => {
          if (data.success) {
            checkedBoxes.forEach(box => {
              const row = box.closest('tr');
              row.remove();
            });
            alert('삭제되었습니다.');
          } else {
            alert('삭제 실패: 서버 오류');
          }

          document.querySelectorAll('.delete-checkbox-column').forEach(td => {
            td.style.display = 'none';
          });

          const firstTh = document.querySelector('thead tr th[data-delete]');
          if (firstTh) firstTh.remove();

          deleteButton.textContent = '삭제';
          selectingMode = false;
        })
        .catch(err => {
          alert('삭제 중 오류 발생');
          console.error(err);
        });
      }
    });
  }

  // ✅ 글쓰기 (Submit)
  if (form) {
    form.addEventListener('submit', function (e) {
      e.preventDefault();

      const title = document.getElementById('title')?.value.trim();
      const comment = document.getElementById('comment')?.value.trim();

      if (!title || !comment) {
        alert('제목과 내용을 모두 입력해주세요.');
        return;
      }

      const formData = new FormData(form);

      fetch(`http://${serverIP}:5002/api/qna`, {
        method: 'POST',
        credentials: 'include',
        body: formData
      })
      .then(res => res.json())
      .then(data => {
        if (data.status === 'success') {
          alert('Q&A가 등록되었습니다.');
          window.location.href = '/qna'; // 목록 페이지로 이동
        } else {
          alert(`등록 실패: ${data.message}`);
        }
      })
      .catch(err => {
        alert('등록 중 오류 발생');
        console.error(err);
      });
    });
  }

  // ✅ 검색 버튼 클릭
  if (searchButton) {
    searchButton.addEventListener('click', () => {
      if (!searchInput) return;
      currentKeyword = searchInput.value.trim();
      currentPage = 1;
      loadQnaList(currentPage, currentKeyword);
    });
  }
  
  if (searchInput) {
    searchInput.addEventListener('keydown', (e) => {
      if (e.key === 'Enter') {
        e.preventDefault();
        currentKeyword = searchInput.value.trim();
        currentPage = 1;
        loadQnaList(currentPage, currentKeyword);
      }
    });
  }
  

  // ✅ QnA 목록 불러오기
  function loadQnaList(page = 1, keyword = '') {
    const url = new URL(`http://${serverIP}:5002/api/qna/`);
    url.searchParams.set('page', page);
    url.searchParams.set('per_page', 10);
    if (keyword) {
      url.searchParams.set('keyword', keyword);
    }

    fetch(url.toString(), {
      method: 'GET',
      credentials: 'include'
    })
    .then(res => res.json())
    .then(data => {
      if (!tbody) return;
      tbody.innerHTML = '';

      if (data.status === 'success' && data.data?.items && data.data.items.length > 0) {
        data.data.items.forEach((post, idx) => {
          const row = document.createElement('tr');
          row.classList.add('clickable-row');
          row.setAttribute('data-no', post.id);

          row.innerHTML = `
            <td class="delete-checkbox-column" style="display: none;">
              <input type="checkbox" class="delete-checkbox" value="${post.id}">
            </td>
            <td>${idx + 1 + (page - 1) * 10}</td>
            <td>
              <a href="/qna/post/${post.id}" style="text-decoration: none; color: inherit;">
                ${post.title}
              </a>
            </td>
            <td>${post.writer || '알 수 없음'}</td>
            <td>${post.created_at}</td>
          `;
          tbody.appendChild(row);
        });
        renderPagination(data.data.page, data.data.total_pages);
      } else {
        tbody.innerHTML = '<tr><td colspan="6" class="text-muted py-4">질문이 없습니다.</td></tr>';
        if (pagination) pagination.innerHTML = '';
      }
    })
    .catch(err => {
      console.error('❌ Q&A 목록 로딩 실패:', err);
      if (tbody) {
        tbody.innerHTML = '<tr><td colspan="6" class="text-danger py-4">목록을 불러오는 데 실패했습니다.</td></tr>';
      }
    });
  }

  // ✅ 페이지네이션 그리기
  function renderPagination(current, total) {
    if (!pagination) return;
    pagination.innerHTML = '';

    for (let i = 1; i <= total; i++) {
      const activeClass = i === current ? "active" : "";
      const pageItem = `
        <li class="page-item ${activeClass}">
          <a class="page-link" href="#" onclick="changePage(${i})">${i}</a>
        </li>
      `;
      pagination.insertAdjacentHTML('beforeend', pageItem);
    }
  }

  // ✅ 페이지 변경
  window.changePage = function (page) {
    currentPage = page;
    loadQnaList(page, currentKeyword);
  };

  // ✅ 페이지 처음 열 때 초기 QnA 목록
  loadQnaList(currentPage);
});
