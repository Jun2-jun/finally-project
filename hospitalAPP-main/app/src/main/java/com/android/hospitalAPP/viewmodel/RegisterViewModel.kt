package com.android.hospitalAPP.viewmodel

import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import com.android.hospitalAPP.data.ApiResult
import com.android.hospitalAPP.data.UserService
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.launch

// ✅ 회원가입 기능을 담당하는 ViewModel
class RegisterViewModel : ViewModel() {

    // UserService 인스턴스 생성 (API 요청 담당)
    private val userService = UserService()

    // 회원가입 상태를 위한 StateFlow (초기값은 Initial)
    private val _registerState = MutableStateFlow<RegisterState>(RegisterState.Initial)
    val registerState: StateFlow<RegisterState> = _registerState

    /**
     * ✅ 회원가입 처리 메서드
     * @param email 이메일
     * @param userId 사용자 ID
     * @param password 비밀번호
     * @param address_detail 상세 주소
     * @param birthdate 생년월일
     * @param phone 전화번호
     * @param address 주소
     */
    fun register(
        email: String,
        userId: String,
        password: String,
        address_detail: String,
        birthdate: String,
        phone: String,
        address: String
    ) {
        viewModelScope.launch {
            // API 요청 전, 로딩 상태로 변경
            _registerState.value = RegisterState.Loading

            try {
                // 회원가입 API 호출
                val result = userService.register(email, userId, password, birthdate, phone, address, address_detail)

                // 결과 처리
                when (result) {
                    is ApiResult.Success -> {
                        // 성공 응답 처리
                        val responseData = result.data
                        val status = responseData.optString("status")
                        val message = responseData.optString("message")

                        if (status == "success") {
                            // 회원가입 성공
                            _registerState.value = RegisterState.Success(message)
                        } else {
                            // 회원가입 실패 (status != success)
                            _registerState.value = RegisterState.Error(message)
                        }
                    }
                    is ApiResult.Error -> {
                        // 오류 응답 처리
                        _registerState.value = RegisterState.Error(result.message)
                    }
                }
            } catch (e: Exception) {
                // 예외 발생
                _registerState.value = RegisterState.Error("회원가입 중 오류가 발생했습니다: ${e.message}")
            }
        }
    }

    /**
     * ✅ 회원가입 상태를 나타내는 sealed class
     */
    sealed class RegisterState {
        object Initial : RegisterState() // 초기 상태
        object Loading : RegisterState() // API 요청 중
        data class Success(val message: String) : RegisterState() // 성공
        data class Error(val message: String) : RegisterState() // 실패 또는 오류
    }
}