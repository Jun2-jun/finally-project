// ReservationHistoryViewModel.kt
package com.android.hospitalAPP.viewmodel

import android.util.Log
import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import com.android.hospitalAPP.data.ApiResult
import com.android.hospitalAPP.data.ReservationService
import com.android.hospitalAPP.data.UserRepository
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.asStateFlow
import kotlinx.coroutines.launch
import org.json.JSONObject

class ReservationHistoryViewModel : ViewModel() {
    private val reservationService = ReservationService()
    private val userRepository = UserRepository.getInstance()

    private val _uiState = MutableStateFlow<ReservationHistoryUiState>(ReservationHistoryUiState.Loading)
    val uiState: StateFlow<ReservationHistoryUiState> = _uiState.asStateFlow()

    fun loadReservations() {
        viewModelScope.launch {
            _uiState.value = ReservationHistoryUiState.Loading

            val currentUser = userRepository.currentUser.value
            if (currentUser == null) {
                _uiState.value = ReservationHistoryUiState.NotLoggedIn
                return@launch
            }

            try {
                val result = reservationService.getUserReservations(currentUser.userId)

                when (result) {
                    is ApiResult.Success -> {
                        val reservations = parseReservationsFromJson(result.data)
                        if (reservations.isEmpty()) {
                            _uiState.value = ReservationHistoryUiState.Empty
                        } else {
                            _uiState.value = ReservationHistoryUiState.Success(reservations)
                        }
                    }
                    is ApiResult.Error -> {
                        _uiState.value = ReservationHistoryUiState.Error(result.message)
                    }
                }
            } catch (e: Exception) {
                _uiState.value = ReservationHistoryUiState.Error("예약 내역을 불러오는 중 오류가 발생했습니다: ${e.message}")
            }
        }
    }

    private fun parseReservationsFromJson(json: JSONObject): List<Reservation> {
        val reservations = mutableListOf<Reservation>()

        try {
            // 전체 JSON 데이터를 로그로 출력
            Log.d("ReservationHistoryVM", "Received JSON: $json")

            val status = json.optString("status")
            val data = json.optJSONArray("data")

            // status와 data 필드의 존재 여부 확인
            Log.d("ReservationHistoryVM", "Status: $status")
            Log.d("ReservationHistoryVM", "Data exists: ${data != null}")

            if (status == "success" && data != null) {
                for (i in 0 until data.length()) {
                    val item = data.getJSONObject(i)
                    val reservation = Reservation(
                        id = item.optString("id", ""),
                        hospital = item.optString("hospital", ""),
                        address = item.optString("address", ""),
                        name = item.optString("name", ""),
                        phone = item.optString("phone", ""),
                        message = item.optString("message", ""),
                        email = item.optString("email", ""),
                        status = item.optString("status", "")
                    )
                    reservations.add(reservation)
                }
            } else {
                Log.e("ReservationHistoryVM", "Invalid JSON structure or status is not success")
            }
        } catch (e: Exception) {
            Log.e("ReservationHistoryVM", "예약 데이터 파싱 중 오류: ${e.message}", e)
        }

        return reservations
    }

    // UI 상태를 나타내는 sealed class
    sealed class ReservationHistoryUiState {
        object Loading : ReservationHistoryUiState()
        object NotLoggedIn : ReservationHistoryUiState()
        object Empty : ReservationHistoryUiState()
        data class Success(val reservations: List<Reservation>) : ReservationHistoryUiState()
        data class Error(val message: String) : ReservationHistoryUiState()
    }
}

data class Reservation(
    val id: String,
    val hospital: String,
    val address: String,
    val name: String,
    val phone: String,
    val message: String,
    val email: String,
    val status: String
)