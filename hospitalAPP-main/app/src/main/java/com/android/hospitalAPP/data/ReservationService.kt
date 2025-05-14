package com.android.hospitalAPP.data

import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.withContext
import org.json.JSONObject

/**
 * 병원 예약 관련 API 요청을 처리하는 서비스 클래스
 */
class ReservationService {

    /**
     * ✅ 병원 예약 API 요청
     * @param userId 사용자 ID
     * @param name 예약자 이름
     * @param phone 연락처
     * @param hospital 병원명
     * @param address 병원 주소
     * @param message 예약 메시지/증상
     * @param email 이메일 (선택)
     * @param reservation_time 예약 시간 (선택)
     * @param timestamp 예약 생성 시간 (기본값: 현재 시간)
     * @return 예약 처리 결과 (ApiResult)
     */
    suspend fun makeReservation(
        userId: String,
        name: String,
        phone: String,
        hospital: String,
        address: String,
        message: String,
        email: String? = null,
        reservation_time: String? = null,  // 추가된 필드
        timestamp: Long = System.currentTimeMillis()
    ): ApiResult<JSONObject> = withContext(Dispatchers.IO) {
        // JSON 요청 본문 생성
        val jsonBody = JSONObject().apply {
            put("user_id", userId.toInt())  // user_id 컬럼에 userId 추가
            put("name", name)
            put("phone", phone)
            put("hospital", hospital)
            put("address", address)
            put("message", message)
            put("reservation_time", reservation_time)
            put("timestamp", timestamp)
            if (!email.isNullOrBlank()) {
                put("email", email)
            }
        }

        // 예약 API POST 요청 실행
        ApiServiceCommon.postRequest(ApiConstants.RESERVATION_URL, jsonBody)
    }

    /**
     * ✅ 예약 내역 조회 API 요청
     * @param userId 사용자 ID
     * @return 예약 내역 조회 결과 (ApiResult)
     */
    suspend fun getUserReservations(userId: String): ApiResult<JSONObject> = withContext(Dispatchers.IO) {
        try {
            // 예약 조회 API URL 구성
            val url = "${ApiConstants.RESERVATION_SEARCH_URL}/$userId"
            // 예약 조회 API GET 요청 실행
            ApiServiceCommon.getRequest(url)
        } catch (e: Exception) {
            // 예외 발생 시 에러 반환
            ApiResult.Error(message = "예약 내역 조회 중 오류 발생: ${e.message}")
        }
    }
}