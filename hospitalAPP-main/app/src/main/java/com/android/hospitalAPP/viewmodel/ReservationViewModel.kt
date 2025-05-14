package com.android.hospitalAPP.viewmodel

import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import com.android.hospitalAPP.data.ApiResult
import com.android.hospitalAPP.data.ReservationService
import com.android.hospitalAPP.data.UserRepository
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.launch

// ✅ 예약 기능을 담당하는 ViewMode
class ReservationViewModel : ViewModel() {
    private val reservationService = ReservationService()
    private val userRepository = UserRepository.getInstance()

    // 예약 상태를 위한 StateFlow (초기값은 Initial)
    private val _reservationState = MutableStateFlow<ReservationState>(ReservationState.Initial)
    val reservationState: StateFlow<ReservationState> = _reservationState

    /**
     * ✅ 예약하기
     * @param hospital 병원 이름
     * @param address 병원 주소
     * @param message 예약 메시지 (증상 등)
     * @param email 이메일 (선택사항)
     * @param reservation_time 예약 시간 (선택사항)
     */
    fun makeReservation(
        hospital: String,
        address: String,
        message: String,
        email: String? = null,
        reservation_time: String? = null
    ) {
        // 현재 로그인된 사용자 확인
        val currentUser = userRepository.currentUser.value
        if (currentUser == null) {
            _reservationState.value = ReservationState.Error("로그인이 필요한 서비스입니다.")
            return
        }

        viewModelScope.launch {
            try {
                // 로딩 상태로 변경
                _reservationState.value = ReservationState.Loading

                // 로그인된 사용자 정보로 예약자 정보 구성
                val userId = currentUser.userId  // userId 가져오기
                val name = currentUser.userName
                val phone = currentUser.phone    // 사용자 실제 전화번호 사용

                // 예약 API 호출
                val result = reservationService.makeReservation(
                    userId = userId,
                    name = name,
                    phone = phone,
                    hospital = hospital,
                    address = address,
                    message = message,
                    email = email,
                    reservation_time= reservation_time
                )

                // 결과 처리
                when (result) {
                    is ApiResult.Success -> {
                        // 성공 응답 처리
                        _reservationState.value = ReservationState.Success("예약이 완료되었습니다.")
                    }
                    is ApiResult.Error -> {
                        // 오류 응답 처리
                        _reservationState.value = ReservationState.Error(result.message)
                    }
                }
            } catch (e: Exception) {
                // 예외 발생
                _reservationState.value = ReservationState.Error("예약 중 오류가 발생했습니다: ${e.message}")
            }
        }
    }

    /**
     * 에러 메시지 초기화
     */
    fun resetState() {
        _reservationState.value = ReservationState.Initial
    }

    /**
     * ✅ 예약 상태를 나타내는 sealed class
     */
    sealed class ReservationState {
        object Initial : ReservationState()
        object Loading : ReservationState()
        data class Success(val message: String) : ReservationState()
        data class Error(val message: String) : ReservationState()
    }
}