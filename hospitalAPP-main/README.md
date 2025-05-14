# 병원 예약 앱 (Hospital Appointment App)

## 📱 프로젝트 소개
이 프로젝트는 Jetpack Compose를 활용한 현대적인 안드로이드 병원 예약 애플리케이션입니다. 사용자가 주변 병원을 검색하고 예약할 수 있으며, 건강 관련 상담, 커뮤니티 기능까지 제공하는 종합 의료 서비스 플랫폼입니다.

## 🚀 주요 기능

### 🏥 병원 검색 및 예약
- **카카오맵 API 활용**: 실시간으로 주변 병원 검색 및 위치 확인
- **예약 시스템**: 간편한 병원 예약 및 예약 내역 관리
- **진료과별 병원 찾기**: 전문 분야별 병원 필터링

### 🤖 AI 건강 상담 (닥터 퓨처)
- **AI 챗봇**: 건강 관련 질문에 대한 실시간 응답
- **건강 체크리스트**: 개인 건강 상태 관리 (개발 중)
- **건강 다이어리**: 증상, 약 복용 기록 관리 (개발 중)

### 👨‍👩‍👧‍👦 커뮤니티
- **Q&A 게시판**: 건강 관련 질문과 답변 공유
- **공지사항**: 중요 정보 및 업데이트 확인
- **게시글 작성**: 사용자 경험 및 정보 공유

### 👤 사용자 관리
- **회원가입/로그인**: 개인화된 서비스 제공
- **마이페이지**: 사용자 정보 관리
- **보안 기능**: 루팅 기기 감지 및 차단

## 🛠️ 기술 스택

### 프론트엔드
- **Jetpack Compose**: 모던 UI 개발
- **Material Design 3**: 직관적이고 일관된 사용자 경험
- **Navigation Component**: 화면 간 이동 관리

### 백엔드 연동
- **RESTful API**: 서버와 클라이언트 간 통신
- **OkHttp**: 네트워크 요청 처리
- **JSON 파싱**: 서버 응답 데이터 처리

### 데이터 관리
- **StateFlow**: 반응형 데이터 처리
- **ViewModel**: UI 데이터 및 상태 관리
- **SharedPreferences**: 로컬 데이터 저장

### 지도 및 위치 서비스
- **카카오맵 SDK**: 지도 표시 및 위치 검색
- **벡터 맵**: 고품질 지도 렌더링

## 📂 프로젝트 구조
```
app/src/main/java/com/example/compose/
├── MainActivity.kt                # 앱 진입점
├── Navigation.kt                  # 앱 화면 간 이동 관리
├── RootCheck.kt                   # 루팅 감지 기능 (보안)
├── Components.kt                  # 공통 UI 컴포넌트 (바텀 네비게이션 등)
├── WithdrawAccountScreen.kt       # 회원 탈퇴 화면
│
├── ui/
│   ├── components/
│   │   ├── BottomNavigation.kt    # 하단 탐색 바
│   │   ├── KakaoMapComponent.kt   # 카카오맵 표시 컴포넌트
│   │   ├── KakaoMapView.kt        # 카카오맵 표시 뷰
│   │   ├── ReservationDialog.kt   # 예약 다이얼로그
│   │   └── SearchBarComponent.kt  # 검색창 컴포넌트
│   │
│   ├── screens/
│   │   ├── HomeScreen.kt          # 홈 화면
│   │   ├── DoctorFutureScreen.kt  # 닥터 퓨처(AI) 화면
│   │   ├── ChatBotScreen.kt       # AI 챗봇 화면
│   │   ├── CommunityScreen.kt     # 커뮤니티 화면
│   │   ├── MyPageScreen.kt        # 마이페이지 화면
│   │   ├── LoginPage.kt           # 로그인 화면
│   │   ├── RegisterPage.kt        # 회원가입 화면
│   │   ├── ProfileManagementScreen.kt  # 프로필 관리 화면
│   │   ├── ChangePasswordScreen.kt     # 비밀번호 변경 화면
│   │   ├── WritePostScreen.kt          # 게시글 작성 화면
│   │   ├── PostDetailScreen.kt         # 게시글 상세 화면
│   │   ├── NoticeDetailScreen.kt       # 공지사항 상세 화면
│   │   ├── HospitalSearchResultScreen.kt  # 병원 검색 결과 화면
│   │   └── ReservationHistoryScreen.kt    # 예약 내역 화면
│   │
│   └── theme/
│       ├── Color.kt               # 색상 정의
│       ├── Theme.kt               # 앱 테마 및 디자인 시스템
│       └── Type.kt                # 타이포그래피 정의
│
├── data/
│   ├── ApiConstants.kt            # API 엔드포인트 상수
│   ├── ApiServiceCommon.kt        # API 통신 공통 로직
│   ├── KakaoMapService.kt         # 카카오맵 API 연동
│   ├── PostRepository.kt          # 게시글 데이터 관리
│   ├── ReservationService.kt      # 예약 관련 API
│   ├── UserRepository.kt          # 사용자 데이터 관리
│   └── UserService.kt             # 사용자 관련 API 요청 처리
│
├── viewmodel/
│   ├── HomeViewModel.kt           # 홈 화면 뷰모델
│   ├── ChatBotViewModel.kt        # 챗봇 화면 뷰모델
│   ├── CommunityViewModel.kt      # 커뮤니티 화면 뷰모델
│   ├── HospitalSearchViewModel.kt # 병원 검색 뷰모델
│   ├── LoginViewModel.kt          # 로그인 뷰모델
│   ├── RegisterViewModel.kt       # 회원가입 뷰모델
│   ├── ProfileManagementViewModel.kt  # 프로필 관리 뷰모델
│   ├── ChangePasswordViewModel.kt     # 비밀번호 변경 뷰모델
│   ├── WithdrawAccountViewModel.kt    # 회원탈퇴 뷰모델
│   ├── ReservationViewModel.kt        # 예약 뷰모델
│   └── ReservationHistoryViewModel.kt # 예약 내역 뷰모델
│
└── util/
    └── SharedPreferencesManager.kt    # 로컬 데이터 저장 관리
```
## 🔒 보안 기능
- **루팅 감지**: 루팅된 기기에서의 실행 방지 (Native C++ 코드 활용)
- **세션 관리**: 안전한 사용자 인증 유지
- **비밀번호 암호화**: 사용자 정보 보호

## 📱 스크린샷

<p align="center">
  <img src="https://github.com/user-attachments/assets/01626143-91b6-4abd-896c-e2a4183c53a1" width="200"/>
  <img src="https://github.com/user-attachments/assets/b1916e3f-a0cc-4306-90b3-4dd2203028d8" width="200"/>
  <img src="https://github.com/user-attachments/assets/498b1790-b55d-46d7-8798-c9d612323bc0" width="200"/>
  <img src="https://github.com/user-attachments/assets/25b6af3a-9826-42d5-9c1a-d2dc0f783011" width="200"/>
</p>


## 🚀 시작하기

### 요구 사항
- Android Studio Narwhal 이상
- Kotlin 1.5.0 이상
- Android SDK 21 이상

### 설치 방법
1. 저장소 클론:
```
git clone https://github.com/Avox-dev/hospitalAPP.git
```

2. Android Studio에서 프로젝트 열기

3. 카카오맵 API 키 설정:
   - `app/src/main/java/com/example/compose/KakaoMapService.kt`에서 API 키 변경
   - `app/src/main/java/com/example/compose/MainActivity.kt`에서 SDK 초기화 키 변경

4. 앱 빌드 및 실행

## 🔌 API 연동
- **기본 URL**: `http://192.168.219.105:5002/api`
- **경로 수정** `data/ApiServiceCommon.kt`
- 다음 API 엔드포인트 사용:
  - 회원 관리: `/users/*`
  - 예약 관리: `/reservations/*`
  - 커뮤니티: `/qna`, `/notices`
  - AI 챗봇: `/ai`

## 📜 라이센스
이 프로젝트는 MIT 라이센스 하에 배포됩니다. 자세한 내용은 `LICENSE` 파일을 참조하세요.


## 🙏 감사의 글
- 카카오맵 API 제공
- Jetpack Compose 팀
