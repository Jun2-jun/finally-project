// UserRepository.kt
package com.android.hospitalAPP.data

import android.content.Context
import kotlinx.coroutines.CoroutineScope
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.asStateFlow
import kotlinx.coroutines.launch
import com.android.hospitalAPP.util.SharedPreferencesManager

class UserRepository {
    private val _currentUser = MutableStateFlow<User?>(null)
    val currentUser: StateFlow<User?> = _currentUser.asStateFlow()
    private var sessionId: String? = null
    private var prefsManager: SharedPreferencesManager? = null

    // UserService 인스턴스
    private val userService = UserService()

    // 컨텍스트 설정 메서드 (Application 컨텍스트 사용해야 함)
    fun setContext(context: Context) {
        if (prefsManager == null) {
            prefsManager = SharedPreferencesManager.getInstance(context)
            // 저장된 세션 ID가 있다면 로드
            val savedSessionId = prefsManager?.getSessionId()
            if (!savedSessionId.isNullOrEmpty()) {
                sessionId = savedSessionId
            }
        }
    }

    fun setSessionId(id: String) {
        sessionId = id
        // SharedPreferences에도 저장
        prefsManager?.saveSessionId(id)
    }

    fun getSessionId(): String? {
        // SharedPreferences에서 세션 ID를 우선적으로 가져옴
        val savedSessionId = prefsManager?.getSessionId()
        return if (!savedSessionId.isNullOrEmpty()) savedSessionId else sessionId
    }

    fun setCurrentUser(user: User) {
        _currentUser.value = user
    }

    // 🔄 UserRepository에 Patient 저장 기능 추가
    fun setPatientInfo(patient: Patient) {
        prefsManager?.savePatientInfo(patient) // 필요 시 SharedPreferences에도 저장 가능
        // 상태 보존이 필요하면 추가로 MutableStateFlow 생성해서 관리 가능
    }

    fun logoutUser() {
        // 서버에 로그아웃 요청 보내기
        CoroutineScope(Dispatchers.IO).launch {
            try {
                // UserService의 logout 메서드 호출
                val result = userService.logout()

                when (result) {
                    is ApiResult.Success -> {
                        // 로그아웃 성공 시 로컬 상태 초기화
                        _currentUser.value = null
                        sessionId = null

                        // 자동 로그인 비활성화 및 모든 정보 삭제
                        prefsManager?.let {
                            // 자동 로그인 설정 해제
                            it.saveLoginInfo("", "", false)
                            // 모든 정보 클리어
                            it.clearAll()
                        }
                    }
                    is ApiResult.Error -> {
                        // 서버 로그아웃 실패 시에도 로컬에서는 로그아웃 처리
                        _currentUser.value = null
                        sessionId = null
                        // 자동 로그인 비활성화 및 모든 정보 삭제
                        prefsManager?.let {
                            it.saveLoginInfo("", "", false)
                            it.clearAll()
                        }
                        println("로그아웃 API 오류: ${result.message}")
                    }
                }
            } catch (e: Exception) {
                // 네트워크 오류 등의 예외 발생 시에도 로컬에서 로그아웃 처리
                _currentUser.value = null
                sessionId = null
                // 자동 로그인 비활성화 및 모든 정보 삭제
                prefsManager?.let {
                    it.saveLoginInfo("", "", false)
                    it.clearAll()
                }
                println("로그아웃 처리 중 예외 발생: ${e.message}")
            }
        }
    }

    fun isLoggedIn(): Boolean {
        return currentUser.value != null
    }

    companion object {
        // 싱글톤 패턴 구현
        private var instance: UserRepository? = null

        fun getInstance(): UserRepository {
            if (instance == null) {
                instance = UserRepository()
            }
            return instance!!
        }
    }
}

// User 데이터 클래스는 변경하지 않음
data class User(
    val userId: String,
    val userName: String = "사용자", // 기본값 설정
    val email: String = "",        // 추가
    val phone: String = "",        // 추가
    val birthdate: String = "",    // 추가
    val address: String = "",      // 추가
    val sessionId: String = "",    // 추가(세션 아이디)
    val address_detail: String = "",// 추가(상세주소)
)
data class Patient(
    /*환자 정보*/
    val bloodType: String,      // 혈액형
    val heightCm: String,        // 키
    val weightKg: String,        // 몸무게
    val allergyInfo: String,    // 알레르기 정보
    val pastIllnesses: String,  // 과거 질병 이력
    val chronicDiseases: String // 만성질환
)
