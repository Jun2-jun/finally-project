let currentPage = 1;
let currentKeyword = '';
const tbody = document.getElementById('noticeTableBody');
const pagination = document.getElementById('pagination');
const searchInput = document.getElementById('search-input');
const searchButton = document.getElementById('search-button');
const serverIP = document.body.dataset.serverIp;
// 🔍 검색 이벤트
if (searchButton) {
  searchButton.addEventListener('click', () => {
    currentKeyword = searchInput.value.trim();
    currentPage = 1;
    loadNoticeList(currentPage, currentKeyword);
  });
}
if (searchInput) {
  searchInput.addEventListener('keydown', (e) => {
    if (e.key === 'Enter') {
      e.preventDefault();
      currentKeyword = searchInput.value.trim();
      currentPage = 1;
      loadNoticeList(currentPage, currentKeyword);
    }
  });
}

// 📥 공지사항 목록 불러오기
function loadNoticeList(page = 1, keyword = '') {
  const url = new URL(`${serverIP}/api/notices`);
  url.searchParams.set('page', page);
  url.searchParams.set('per_page', 10);
  if (keyword) url.searchParams.set('keyword', keyword);

  fetch(url, {
    method: 'GET',
    credentials: 'include'
  })
    .then(res => res.json())
    .then(data => {
      if (data.status === 'success' && data.data.items?.length > 0) {
        renderNotices(data.data.items, page);
        renderPagination(data.data.page, data.data.total_pages);
      } else {
        tbody.innerHTML = '<tr><td colspan="5" class="text-muted py-4">공지사항이 없습니다.</td></tr>';
        if (pagination) pagination.innerHTML = '';
      }
    })
    .catch(err => {
      console.error('❌ 공지사항 로딩 실패:', err);
      tbody.innerHTML = '<tr><td colspan="5" class="text-danger py-4">공지사항을 불러오는 데 실패했습니다.</td></tr>';
    });
}

function renderNotices(notices, page) {
  tbody.innerHTML = '';
  notices.forEach((notice, idx) => {
    const row = document.createElement('tr');
    row.classList.add('clickable-row');
    row.setAttribute('data-no', notice.id);
    row.innerHTML = `
      <td>${idx + 1 + (page - 1) * 10}</td>
      <td>${notice.title}</td>
      <td>${notice.author || '관리자'}</td>
      <td>${notice.created_at}</td>
      <td>${notice.views}</td>
    `;
    row.addEventListener('click', () => {
      window.location.href = `/notice/post/${notice.id}`;
    });
    tbody.appendChild(row);
  });
}

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

window.changePage = function (page) {
  currentPage = page;
  loadNoticeList(page, currentKeyword);
};

// ✅ 초기 로딩
loadNoticeList(currentPage);
