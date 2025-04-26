# finally-project
# 모듈화된 API 서버 구조 설명

기존 Flask API 서버를 모듈화하여 더 유지보수하기 쉽고, 확장 가능한 구조로 개선했습니다. 다음은 각 디렉토리와 파일의 역할과 실행 방법에 대한 설명입니다.

## 디렉토리 구조

```
finally-project-api/
├── api/
│   ├── __init__.py                  # Blueprint 등록 등 API 모듈 초기화
│   ├── ai_endpoints.py              # AI 관련 API 엔드포인트
│   ├── auth.py                      # 인증/로그인 관련 API
│   ├── check_login.py               # 로그인 체크 API
│   ├── current_user.py              # 현재 로그인 유저 정보 제공
│   ├── dashboard.py                 # 대시보드 관련 API
│   ├── mypage.py                    # 마이페이지 관련 API
│   ├── notices.py                   # 공지사항 관련 API
│   ├── qna.py                       # QnA 관련 API
│   ├── reservations.py              # 예약 관리 API
│   └── users.py                     # 회원가입, 회원 정보 API
│
├── models/
│   ├── __init__.py                  # 모델 초기화
│   ├── notice.py                    # 공지사항 모델
│   ├── qna.py                       # QnA 모델
│   ├── reservation.py               # 예약 모델
│   └── user.py                      # 유저 모델
│
├── static/                          # 정적 파일 폴더 (이미지 등)
│
├── utils/
│   ├── __init__.py
│   ├── ai.py                        # AI 기능 유틸
│   ├── auth.py                      # 인증 관련 유틸 함수
│   ├── email.py                     # 이메일 전송 유틸
│   ├── helpers.py                   # 공통 도우미 함수
│
├── app.py                           # 앱 실행 및 Flask 앱 생성
├── config.py                        # 환경별 설정 (development, production 등)
├── extensions.py                    # DB, 메일, 세션 등 확장 기능 초기화
├── requirements.txt                 # 프로젝트 의존 패키지 목록
└── README.md                        # 프로젝트 설명 문서
```

## 각 파일의 역할

### 주요 파일
1. **app.py**: 애플리케이션의 메인 진입점으로, Flask 앱을 생성하고 초기화합니다.
2. **config.py**: 환경별 설정(개발, 프로덕션)을 관리합니다.
3. **extensions.py**: Flask 확장 프로그램(MySQL, Mail 등)을 초기화합니다.

### 유틸리티 (utils/)
1. **auth.py**: 인증 관련 함수(비밀번호 해싱, 검증 등)를 포함합니다.
2. **email.py**: 이메일 발송 함수를 제공합니다.
3. **helpers.py**: 날짜 형식화, 파일 업로드 등 공통 유틸리티 함수를 포함합니다.
4. **ai.py**: Gemini API 호출 함수를 제공합니다.

### 모델 (models/)
데이터베이스 작업을 담당하는 함수들을 포함합니다:
1. **user.py**: 사용자 관련 데이터베이스 작업
2. **reservation.py**: 예약 관련 데이터베이스 작업
3. **qna.py**: Q&A 게시판 관련 데이터베이스 작업
4. **notice.py**: 공지사항 관련 데이터베이스 작업

### API 엔드포인트 (api/)
각 엔드포인트 그룹별로 파일을 분리했습니다:
1. **POST /api/users/register** : 회원가입
2. **POST /api/users/login** : 로그인 (세션 기반)
3. **POST /api/users/logout** :	로그아웃
4. **GET /api/users/**	: 사용자 목록 조회 (관리자용)
5. **POST /api/users/update** :	사용자 정보 수정
6. **POST /api/users/change-password** :	비밀번호 변경
7. **POST /api/users/check-password** :	비밀번호 일치 여부 확인
8. **GET /api/qna/** :	Q&A 게시판 목록 조회
9. **POST /api/qna/** :	Q&A 게시글 작성
10. **GET /api/qna/<id>** :	특정 Q&A 게시글 조회
11. **DELETE /api/qna/<id>** :	Q&A 게시글 삭제 (관리자)
12. **GET /api/notices/**	: 공지사항 목록 조회
13. **POST /api/reservations/** :	예약 등록

## 실행 방법

1. 필요한 패키지 설치:
```bash
pip install flask flask-mysqldb flask-cors flask-mail flask-session redis bcrypt requests
```

2. 서버 실행:
```bash
python app.py
```

## 이점

1. **모듈화된 구조**: 각 기능이 분리되어 있어 유지보수가 용이합니다.
2. **확장성**: 새로운 기능을 추가할 때 해당 모듈만 수정하면 됩니다.
3. **가독성**: 코드가 목적별로 분리되어 있어 이해하기 쉽습니다.
4. **테스트 용이성**: 각 모듈을 독립적으로 테스트할 수 있습니다.
5. **협업 향상**: 여러 개발자가 동시에 다른 모듈을 작업할 수 있습니다.
