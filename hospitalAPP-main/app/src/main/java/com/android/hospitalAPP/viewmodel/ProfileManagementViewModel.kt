// ProfileManagementViewModel.kt
package com.android.hospitalAPP.viewmodel

import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import com.android.hospitalAPP.data.ApiResult
import com.android.hospitalAPP.data.UserRepository
import com.android.hospitalAPP.data.UserService
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.launch
import java.time.LocalDate
import java.time.ZoneId
import java.time.format.DateTimeFormatter
import java.util.Locale

// ✅ 프로필 관리 (회원 정보 수정) 기능을 담당하는 ViewModel
class ProfileManagementViewModel : ViewModel() {

    private val userService = UserService() // 사용자 API 서비스 인스턴스

    // 화면에 보여줄 업데이트 상태
    private val _updateState = MutableStateFlow<UpdateState>(UpdateState.Initial)
    val updateUiState: StateFlow<UpdateState> = _updateState

    // 프로필 수정 성공 여부 플래그
    private val _isEditSuccess = MutableStateFlow(false)
    val isEditSuccess: StateFlow<Boolean> = _isEditSuccess

    /**
     * ✅ 사용자 정보 업데이트 요청
     * @param email 이메일
     * @param phone 전화번호
     * @param birthdate 생년월일
     * @param address 주소
     * @param address_detail 상세 주소
     */
    fun update(
        email: String,
        phone: String,
        birthdate: String,
        address: String,
        address_detail: String
    ) {
        viewModelScope.launch {
            // 1) 수정 시작할 때 성공 플래그 초기화
            _isEditSuccess.value = false
            // 2) 로딩 상태로 전환
            _updateState.value = UpdateState.Loading

            try {
                // 서버에 사용자 정보 업데이트 요청
                val result = userService.updateUserInfo(email, phone, birthdate, address, address_detail)

                when (result) {
                    is ApiResult.Success -> {
                        val responseData = result.data
                        val status = responseData.optString("status")
                        val message = responseData.optString("message")

                        if (status == "success") {

                            // 현재 로그인한 사용자 정보 가져오기
                            val currentUser = UserRepository.getInstance().currentUser.value

                            if (currentUser != null) {
                                // ✅ 생년월일 포맷 변환 (yyyy-MM-dd → RFC 1123 GMT 표준 포맷)
                                val inputFormatter = DateTimeFormatter.ofPattern("yyyy-MM-dd") // 예: 1234-12-12
                                val localDate = LocalDate.parse(birthdate, inputFormatter)
                                val gmtDateTime = localDate
                                    .atStartOfDay(ZoneId.of("GMT"))  // GMT 기준 시간
                                    .format(DateTimeFormatter.RFC_1123_DATE_TIME.withLocale(Locale.US))  // Tue, 12 Dec 1234 00:00:00 GMT

                                // ✅ 수정된 사용자 정보 로컬에 저장
                                val updatedUser = currentUser.copy(
                                    email = email,
                                    phone = phone,
                                    birthdate = gmtDateTime,
                                    address = address,
                                    address_detail = address_detail
                                )
                                UserRepository.getInstance().setCurrentUser(updatedUser)

                            // 3) 업데이트 성공 상태로 변경
                            _updateState.value = UpdateState.Success(message)
                                // 4) 성공 플래그 true로 변경
                                _isEditSuccess.value = true
                            }



                        } else {
                            // status가 success가 아닐 때 에러 처리
                            _updateState.value = UpdateState.Error(message)
                        }
                    }
                    is ApiResult.Error -> {
                        // 서버 요청 실패 시
                        _updateState.value = UpdateState.Error(result.message)
                    }
                }
            } catch (e: Exception) {
                // 예외 발생 시
                _updateState.value = UpdateState.Error("정보 수정 중 오류 발생: ${e.message}")
            }
        }
    }

    /**
     * ✅ 수정 성공 플래그 초기화
     * (UI에서 상태를 다시 쓸 수 있게 초기화)
     */
    fun clearEditSuccess() {
        _isEditSuccess.value = false
    }

    /**
     * ✅ 화면에 표시할 업데이트 상태를 나타내는 sealed class
     */
    sealed class UpdateState {
        object Initial : UpdateState()
        object Loading : UpdateState()
        data class Success(val message: String) : UpdateState()
        data class Error(val message: String) : UpdateState()
    }
}
