# finally-project
# 모듈화된 API 서버 구조 설명

기존 Flask API 서버를 모듈화하여 더 유지보수하기 쉽고, 확장 가능한 구조로 개선했습니다. 다음은 각 디렉토리와 파일의 역할과 실행 방법에 대한 설명입니다.

## 디렉토리 구조

```
doctor_future/
├── app.py                  # 메인 애플리케이션 진입점
├── config.py               # 환경설정
├── extensions.py           # Flask 확장 초기화
├── utils/                  # 유틸리티 함수
│   ├── __init__.py
│   ├── email.py            # 이메일 유틸리티 함수
│   ├── auth.py             # 인증 유틸리티
│   ├── helpers.py          # 일반 헬퍼 함수
│   └── ai.py               # AI API 통합
├── api/                    # API 엔드포인트
│   ├── __init__.py         # API Blueprint 초기화
│   ├── users.py            # 사용자 관련 엔드포인트
│   ├── reservations.py     # 예약 관련 엔드포인트
│   ├── dashboard.py        # 대시보드 관련 엔드포인트
│   ├── qna.py              # Q&A 관련 엔드포인트
│   ├── notices.py          # 공지사항 관련 엔드포인트
│   └── ai_endpoints.py     # AI 관련 엔드포인트
├── models/                 # 데이터베이스 모델 함수
│   ├── __init__.py
│   ├── user.py             # 사용자 모델 함수
│   ├── reservation.py      # 예약 모델 함수
│   ├── qna.py              # Q&A 모델 함수
│   └── notice.py           # 공지사항 모델 함수
└── static/
    └── uploads/            # 파일 업로드 디렉토리
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
1. **users.py**: 사용자 관리(로그인, 회원가입 등) API
2. **reservations.py**: 예약 관련 API
3. **dashboard.py**: 관리자 대시보드 API
4. **qna.py**: Q&A 게시판 API
5. **notices.py**: 공지사항 API
6. **ai_endpoints.py**: AI 관련 API

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
