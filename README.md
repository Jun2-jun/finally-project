# 🏥 DoctorFuture 병원 예약 & 게시판 시스템

Flask 기반의 병원 예약 및 사용자 관리 시스템입니다. 공지사항 및 Q&A 기능을 포함한 프론트엔드 + 백엔드 통합 구조로 구성되어 있으며, 기능별 모듈화로 유지보수성과 확장성을 고려했습니다.

---

## 📁 templates/ 디렉토리 구조

```text
templates/
├── AI/
│   └── chatbot.html           # AI 챗봇 관련 페이지
├── editor/
│   └── editor.html            # 에디터 공통 템플릿 (Q&A, 공지에서 import됨)
├── notice/
│   ├── notice.html            # 공지사항 목록 페이지
│   ├── notice_write.html      # 공지사항 작성 페이지
│   └── notice_detail.html     # 공지사항 상세보기
├── qna/
│   ├── qna.html               # Q&A 게시판 목록
│   ├── qna_write.html         # Q&A 글쓰기 페이지
│   └── qna_detail.html        # Q&A 상세보기
├── sidebar/
│   └── sidebar.html           # 사이드바 공통 컴포넌트
├── auth/
│   ├── login.html             # 로그인 페이지
│   ├── register.html          # 회원가입 페이지
│   └── find.html              # 비밀번호 찾기
├── mypage.html                # 마이페이지 (내 정보 수정)
├── reserve.html               # 진료 예약 페이지
├── dashboard.html             # 관리자용 대시보드
└── index.html                 # 홈 또는 루트 페이지





## 💻 기능별 HTML 경로 & JS 흐름 요약

| 기능             | HTML 경로                              | JS 연동 or 설명                         |
|------------------|-----------------------------------------|------------------------------------------|
| ✅ 회원가입       | `auth/register.html`                   | 입력 폼 → `/api/users/register` POST     |
| ✅ 로그인         | `auth/login.html`                      | 로그인 시 세션 저장                     |
| ✅ 마이페이지     | `mypage.html`                          | 로그인 사용자 정보 fetch & 수정        |
| ✅ 예약하기       | `reserve.html`                         | 예약 정보 `/api/reservations`로 저장    |
| ✅ 공지사항 목록   | `notice/notice.html`                  | 공지 리스트 fetch 및 표시               |
| ✅ 공지사항 작성   | `notice/notice_write.html`            | 에디터 포함 작성 후 POST                |
| ✅ Q&A 목록       | `qna/qna.html`                         | 게시글 리스트 + 삭제 (`qna.js`)         |
| ✅ Q&A 작성       | `qna/qna_write.html`                  | 에디터 + 이미지 업로드 (`qna_editor.js`)|
| ✅ Q&A 상세       | `qna/qna_detail.html`                 | 게시글 상세 내용 조회                   |
| ✅ 비밀번호 찾기   | `auth/find.html`                      | 이메일/아이디로 비밀번호 찾기 구현      |

---

## ⚙️ 실행 방법

```bash
# 가상환경 생성 및 실행
python -m venv venv
source venv/bin/activate        # Windows는 venv\Scripts\activate

# 필요 패키지 설치
pip install -r requirements.txt

# 앱 실행
python app.py
```
## 전체 흐름 요약

**브라우저 요청**
    **↓**
**Flask Blueprint API (@api.route)**
    **↓**
**DB 모델 호출 (models/*.py)**
    **↓**
**DB(MySQL) 쿼리 실행**
    **↓**
**결과 리턴 (JSON 응답)**










