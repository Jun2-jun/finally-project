package com.android.hospitalAPP.viewmodel

import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import com.android.hospitalAPP.data.ApiResult
import com.android.hospitalAPP.data.UserService
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.launch

class ChangePasswordViewModel : ViewModel() {
    // UserService 인스턴스 생성
    private val userService = UserService()

    // 비밀번호 상태를 위한 StateFlow
    private val _updatePwdState = MutableStateFlow<UpdatePwdState>(UpdatePwdState.Initial)
    val updatePwdState: StateFlow<UpdatePwdState> = _updatePwdState

    // 비밀번호 변경 처리
    fun updatePwd(current_password: String, new_password: String) {
        viewModelScope.launch {
            _updatePwdState.value = UpdatePwdState.Loading

            try {
                // 비밀번호 변경 API 호출
                val result = userService.updatePwd(current_password, new_password)

                // 결과 처리
                when (result) {
                    is ApiResult.Success -> {
                        // 성공 응답 처리
                        val responseData = result.data
                        val status = responseData.optString("status")
                        val message = responseData.optString("message")

                        if (status == "success") {
                            _updatePwdState.value = UpdatePwdState.Success(message)
                        } else {
                            _updatePwdState.value = UpdatePwdState.Error(message)
                        }
                    }
                    is ApiResult.Error -> {
                        // 오류 응답 처리
                        _updatePwdState.value = UpdatePwdState.Error(result.message)
                    }
                }
            } catch (e: Exception) {
                // 예외 발생
                _updatePwdState.value = UpdatePwdState.Error("비밀번호 변경 중 오류가 발생했습니다: ${e.message}")
            }
        }
    }

    // 비밀번호 변경 상태를 나타내는 sealed class
    sealed class UpdatePwdState {
        object Initial : UpdatePwdState()
        object Loading : UpdatePwdState()
        data class Success(val message: String) : UpdatePwdState()
        data class Error(val message: String) : UpdatePwdState()
    }

    // 이메일 코드 전송 처리
    fun sendEmailCode(email: String) {
        viewModelScope.launch {
            try {
                val result = userService.sendVerificationCode(email)
                when (result) {
                    is ApiResult.Success -> {
                        val responseData = result.data
                        val status = responseData.optString("status")
                        val message = responseData.optString("message")

                        if (status == "success") {
                            println("✅ 이메일 전송 성공: $message")
                        } else {
                            println("❌ 전송 실패: $message")
                        }
                    }
                    is ApiResult.Error -> {
                        println("❌ 서버 오류: ${result.message}")
                    }
                }
            } catch (e: Exception) {
                println("❌ 예외 발생: ${e.message}")
            }
        }
    }

    // 이메일 코드 인증 처리
    fun verifyCode(code: String) {
        viewModelScope.launch {
            try {
                val result = userService.VerifyCode(code)
                when (result) {
                    is ApiResult.Success -> {
                        val responseData = result.data
                        val status = responseData.optString("status")
                        val message = responseData.optString("message")

                        if (status == "success") {
                            println("✅ 이메일 인증 성공: $message")
                        } else {
                            println("❌ 인증 실패: $message")
                        }
                    }
                    is ApiResult.Error -> {
                        println("❌ 서버 오류: ${result.message}")
                    }
                }
            } catch (e: Exception) {
                println("❌ 예외 발생: ${e.message}")
            }
        }
    }
}