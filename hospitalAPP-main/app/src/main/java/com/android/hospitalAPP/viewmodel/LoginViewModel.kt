// LoginViewModel.kt
package com.android.hospitalAPP.viewmodel

import android.app.Application
import androidx.lifecycle.AndroidViewModel
import androidx.lifecycle.viewModelScope
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.asStateFlow
import kotlinx.coroutines.launch
import kotlinx.coroutines.delay
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.withContext
import com.android.hospitalAPP.data.User
import com.android.hospitalAPP.data.UserRepository
import com.android.hospitalAPP.data.ApiResult
import com.android.hospitalAPP.data.UserService
import com.android.hospitalAPP.util.SharedPreferencesManager

// ✅ 로그인 처리를 담당하는 ViewModel (Application 컨텍스트를 사용하기 위해 AndroidViewModel 상속)
class LoginViewModel(application: Application) : AndroidViewModel(application) {
    private val userRepository = UserRepository.getInstance() // 유저 정보 저장소
    private val userService = UserService() // 로그인 API 호출용
    private val prefsManager = SharedPreferencesManager.getInstance(application) // SharedPreferences 관리자

    // 로그인 상태를 관리하는 StateFlow
    private val _loginState = MutableStateFlow<LoginState>(LoginState.Initial)
    val loginState: StateFlow<LoginState> = _loginState.asStateFlow()

    // 사용자 ID, 비밀번호, 자동 로그인 상태를 관리하는 StateFlow
    private val _userId = MutableStateFlow(prefsManager.getUserId())
    val userId: StateFlow<String> = _userId.asStateFlow()

    private val _password = MutableStateFlow(prefsManager.getPassword())
    val password: StateFlow<String> = _password.asStateFlow()

    private val _rememberMe = MutableStateFlow(prefsManager.isAutoLoginEnabled())
    val rememberMe: StateFlow<Boolean> = _rememberMe.asStateFlow()

    init {
        // 앱 시작 시 자동 로그인 처리
        checkAutoLogin()
    }

    /**
     * 자동 로그인 상태 확인 및 처리
     */
    private fun checkAutoLogin() {
        viewModelScope.launch {
            if (prefsManager.isAutoLoginEnabled()) {
                val savedUserId = prefsManager.getUserId()
                val savedPassword = prefsManager.getPassword()

                if (savedUserId.isNotEmpty() && savedPassword.isNotEmpty()) {
                    login(savedUserId, savedPassword, true)
                }
            }
        }
    }

    /**
     * 로그인 상태 값 업데이트
     */
    fun updateUserId(userId: String) {
        _userId.value = userId
    }

    fun updatePassword(password: String) {
        _password.value = password
    }

    fun updateRememberMe(rememberMe: Boolean) {
        _rememberMe.value = rememberMe
    }

    /**
     * ✅ 로그인 처리
     * @param userId 사용자 ID
     * @param password 비밀번호
     * @param isAutoLogin 자동 로그인 여부 (기본값: rememberMe.value)
     */
    fun login(
        userId: String = _userId.value,
        password: String = _password.value,
        isAutoLogin: Boolean = _rememberMe.value
    ) {
        viewModelScope.launch {
            _loginState.value = LoginState.Loading // 로딩 상태 표시

            val maxRetries = 3 // 최대 재시도 횟수
            var retryCount = 0
            var lastException: Exception? = null

            // 재시도 로직
            while (retryCount < maxRetries) {
                try {
                    val result = withContext(Dispatchers.IO) {
                        userService.login(userId, password)
                    }

                    when (result) {
                        is ApiResult.Success -> {
                            val responseData = result.data
                            val status = responseData.optString("status")
                            val message = responseData.optString("message")

                            val sessionId = responseData.optString("session", null)

                            if (status == "success" && sessionId != null) {
                                // 사용자 정보 파싱
                                val userData = responseData.optJSONObject("data")

                                if (userData != null) {
                                    val id = userData.optInt("id", -1).toString()
                                    val username = userData.optString("username", "")
                                    val email = userData.optString("email", "")
                                    val phone = userData.optString("phone", "")
                                    val birthdate = userData.optString("birthdate", "")
                                    val address = userData.optString("address", "")
                                    val address_detail = userData.optString("address_detail", "")

                                    // 자동 로그인 정보 저장
                                    if (isAutoLogin) {
                                        prefsManager.saveLoginInfo(userId, password, true)
                                    } else {
                                        prefsManager.clearLoginInfo() // 자동 로그인 비활성화 시 정보 삭제
                                    }

                                    // 세션 ID 항상 저장
                                    prefsManager.saveSessionId(sessionId)

                                    // ✅ UserRepository에 로그인 사용자 정보 저장
                                    userRepository.setCurrentUser(
                                        User(
                                            userId = id,
                                            userName = username,
                                            email = email,
                                            phone = phone,
                                            birthdate = birthdate,
                                            address = address,
                                            sessionId = sessionId,
                                            address_detail = address_detail
                                        )
                                    )
                                    userRepository.setSessionId(sessionId)
                                    _loginState.value = LoginState.Success(message)
                                } else {
                                    _loginState.value = LoginState.Error("사용자 정보를 불러오는데 실패했습니다.")
                                }
                            } else if (sessionId != null) {
                                _loginState.value = LoginState.Error(message)
                            } else {
                                _loginState.value = LoginState.Error("세션 정보를 불러오는데 실패했습니다")
                            }
                            return@launch // 성공했으면 바로 종료
                        }

                        is ApiResult.Error -> {
                            // 서버에서 에러 반환
                            lastException = Exception(result.message)
                        }
                    }
                } catch (e: Exception) {
                    // 네트워크 오류 등 예외 발생
                    lastException = e
                }

                // 실패했을 때 재시도 로직
                retryCount++
                if (retryCount < maxRetries) {
                    delay(1000L * retryCount) // 점점 대기시간 늘려서 재시도
                }
            }

            // 최종 실패 처리
            _loginState.value = LoginState.Error("로그인 중 오류가 발생했습니다: ${lastException?.message ?: "알 수 없는 오류"}")
        }
    }

    /**
     * 로그아웃 처리
     */
    fun logout() {
        viewModelScope.launch {
            // rememberMe 상태를 false로 업데이트
            _rememberMe.value = false

            // UserRepository의 logoutUser 호출
            userRepository.logoutUser()
        }
    }

    /**
     * ✅ 로그인 상태를 표현하는 sealed class
     */
    sealed class LoginState {
        object Initial : LoginState() // 초기 상태
        object Loading : LoginState() // 로딩 중
        data class Success(val message: String) : LoginState() // 성공 (메시지 포함)
        data class Error(val message: String) : LoginState() // 실패 (에러 메시지 포함)
    }
}