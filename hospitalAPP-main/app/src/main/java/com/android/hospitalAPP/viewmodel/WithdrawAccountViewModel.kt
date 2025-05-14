package com.android.hospitalAPP.viewmodel

import androidx.lifecycle.ViewModel
import com.android.hospitalAPP.data.ApiResult
import com.android.hospitalAPP.data.UserRepository
import com.android.hospitalAPP.data.UserService
import kotlinx.coroutines.launch
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.State
import androidx.lifecycle.viewModelScope

// ✅ 회원 탈퇴 로직을 담당하는 ViewModel
class WithdrawAccountViewModel : ViewModel() {
    private val userService = UserService()

    // 탈퇴 결과를 담을 State (초기값은 null)
    private val _withdrawResult = mutableStateOf<ApiResult<Unit>?>(null)
    val withdrawResult: State<ApiResult<Unit>?> = _withdrawResult

    // ✅ 회원 탈퇴 메서드
    fun withdrawAccount(currentPassword: String) {
        viewModelScope.launch {
            // 서버에 탈퇴 요청
            val result = userService.withdrawAccount(currentPassword)

            when (result) {
                is ApiResult.Success -> {
                    // 탈퇴 성공 시
                    val currentUser = UserRepository.getInstance().currentUser.value
                    if (currentUser != null) {
                        userService.logout()
                        // 유저 정보를 초기화 (기본값으로 설정)
                        val updatedUser = currentUser.copy(
                            userId = "",
                            userName = "사용자",
                            email = "",
                            phone = "",
                            birthdate = "",
                            address = "",
                            address_detail = "",
                            sessionId = ""
                        )
                        UserRepository.getInstance().setCurrentUser(updatedUser)
                    }
                    _withdrawResult.value = ApiResult.Success(Unit)
                }
                is ApiResult.Error -> {
                    // 탈퇴 실패 시 에러 결과 설정
                    _withdrawResult.value = result
                }
            }
        }
    }
}