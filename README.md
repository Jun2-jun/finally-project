
# Doctor Future 프로젝트 환경설정

## 1. 필수 프로그램 설치

### Redis 설치
- [Redis 다운로드 (Microsoft Archive)](https://github.com/microsoftarchive/redis/releases)
- 설치 시 **환경변수 등록** 체크

### MySQL 설치
- [MySQL 다운로드](https://dev.mysql.com/downloads/installer/)
- 설치 시 루트 비밀번호를 **doctor123!** 으로 설정

---

## 2. 데이터베이스 설정

### 2-1. 데이터베이스 생성

```sql
CREATE DATABASE doctor_future;
```

### 2-2. 테이블 생성

```sql
CREATE TABLE users (
  id INT AUTO_INCREMENT PRIMARY KEY,
  username VARCHAR(255) NOT NULL,
  password VARCHAR(255) NOT NULL,
  email VARCHAR(255) NOT NULL,
  birthdate DATE,
  phone VARCHAR(255),
  address VARCHAR(255),
  address_detail VARCHAR(255),
  created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  admin TINYINT(1) NOT NULL DEFAULT 0
);

CREATE TABLE notice (
  id INT AUTO_INCREMENT PRIMARY KEY,
  title VARCHAR(255) NOT NULL,
  comment TEXT NOT NULL,
  image_urls JSON,
  user_id INT,
  created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  views INT DEFAULT 0,
  FOREIGN KEY (user_id) REFERENCES users(id)
);

CREATE TABLE qna (
  id INT AUTO_INCREMENT PRIMARY KEY,
  user_id INT,
  title VARCHAR(255) NOT NULL,
  comment TEXT NOT NULL,
  image_urls JSON,
  writer VARCHAR(100) NOT NULL DEFAULT '익명',
  created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (user_id) REFERENCES users(id)
);

CREATE TABLE qna_comments (
  id INT(11) NOT NULL AUTO_INCREMENT PRIMARY KEY,
  qna_id INT(11) NOT NULL,
  user_id INT(11) NOT NULL,
  comment TEXT NOT NULL,
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
  parent_id INT(11) DEFAULT NULL,
  FOREIGN KEY (qna_id) REFERENCES qna(id) ON DELETE CASCADE,
  FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

CREATE TABLE reservations (
  id INT AUTO_INCREMENT PRIMARY KEY,
  user_id INT,
  name VARCHAR(255) NOT NULL,
  phone VARCHAR(255) NOT NULL,
  hospital VARCHAR(255) NOT NULL,
  address VARCHAR(255) NOT NULL,
  message TEXT,
  email VARCHAR(255),
  created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  reservation_time DATETIME,
  FOREIGN KEY (user_id) REFERENCES users(id)
);

CREATE TABLE PatientSensitiveInfo (
  user_id INT NOT NULL PRIMARY KEY,
  blood_type VARCHAR(10),
  height_cm TEXT,
  weight_kg TEXT,
  allergy_info TEXT,
  past_illnesses TEXT,
  chronic_diseases TEXT,
  medications TEXT,
  smoking_status VARCHAR(20),
  FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);
```

---

## 3. 파이썬 가상환경 설정 및 패키지 설치

### 3-1. 가상환경 생성 및 활성화

```bash
python -m venv venv
./venv/Scripts/activate
```

### 3-2. 필수 패키지 설치

```bash
pip install flask flask_cors pycryptodome flask_mail redis requests flask_mysqldb flask_session mysql mysql-connector-python
```

---

## 4. 서버 설정

### 4-1. IP 수정
- `web/app.py` 및 `api/app.py` 파일 내의 `yourIp` 부분을 실제 서버 IP로 수정합니다.

### 4-2. 병원 예약 기능 관련
- 병원 예약 기능에 대한 API 연동을 원할 경우 **서버 IP**를 알려주시면 등록해드립니다.

---

## 5. 서버 실행 방법

### 5-1. 웹 서버 실행

```bash
cd web
python app.py
```

### 5-2. API 서버 실행

```bash
cd api
python app.py
```

---

> 🔔 참고사항
> 
> - MySQL과 Redis가 정상적으로 실행되고 있어야 서버가 정상 작동합니다.
> - 서버 실행 후, 웹과 API가 각각 분리되어 운영됩니다.

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
