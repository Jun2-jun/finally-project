// ChatBotViewModel.kt
package com.android.hospitalAPP.viewmodel

import android.util.Log
import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import com.android.hospitalAPP.data.ApiConstants
import com.android.hospitalAPP.data.ApiResult
import com.android.hospitalAPP.data.ApiServiceCommon
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.asStateFlow
import kotlinx.coroutines.launch
import kotlinx.coroutines.withContext
import org.json.JSONObject

data class ChatMessage(
    val text: String,
    val isFromUser: Boolean,
    val timestamp: Long = System.currentTimeMillis()
)

class ChatBotViewModel : ViewModel() {
    // 채팅 메시지 목록
    private val _messages = MutableStateFlow<List<ChatMessage>>(emptyList())
    val messages: StateFlow<List<ChatMessage>> = _messages.asStateFlow()

    // 로딩 상태
    private val _isLoading = MutableStateFlow(false)
    val isLoading: StateFlow<Boolean> = _isLoading.asStateFlow()

    // API 서버 URL
    private val chatApiUrl = ApiConstants.CHATBOT_URL

    // 사용자 메시지 전송
    fun sendMessage(message: String) {
        viewModelScope.launch {
            // 사용자 메시지 추가
            addMessage(message, true)

            // API 호출 시작 (로딩 상태 변경)
            _isLoading.value = true

            try {
                // API 호출
                val response = callChatApi(message)

                // 응답 추가
                addMessage(response, false)
            } catch (e: Exception) {
                // 오류 발생 시
                addMessage("죄송합니다. 응답을 받아오는 중 오류가 발생했습니다: ${e.message}", false)
            } finally {
                // 로딩 상태 해제
                _isLoading.value = false
            }
        }
    }

    // 메시지 추가 함수
    private fun addMessage(text: String, isFromUser: Boolean) {
        val newMessage = ChatMessage(text, isFromUser)
        _messages.value = _messages.value + newMessage
    }

    private suspend fun callChatApi(message: String): String = withContext(Dispatchers.IO) {
        try {
            // API 요청 본문 생성
            val jsonBody = JSONObject().apply {
                put("prompt", message)
            }

            Log.d("ChatAPI", "요청 데이터: $jsonBody")

            // ApiServiceCommon을 사용하여 POST 요청 전송
            val result = ApiServiceCommon.postRequest(chatApiUrl, jsonBody)

            when (result) {
                is ApiResult.Success -> {
                    val responseData = result.data
                    Log.d("ChatAPI", "원본 응답: $responseData")

                    try {
                        if (responseData.has("status") && responseData.getString("status") == "success") {
                            if (responseData.has("data")) {
                                val dataObject = responseData.getJSONObject("data")

                                if (dataObject.has("candidates") && dataObject.getJSONArray("candidates").length() > 0) {
                                    val candidate = dataObject.getJSONArray("candidates").getJSONObject(0)

                                    if (candidate.has("content")) {
                                        val content = candidate.getJSONObject("content")

                                        if (content.has("parts") && content.getJSONArray("parts").length() > 0) {
                                            val part = content.getJSONArray("parts").getJSONObject(0)

                                            if (part.has("text")) {
                                                return@withContext part.getString("text")
                                            }
                                        }
                                    }
                                }
                            }
                        }

                        // 여기까지 왔다면 파싱 과정에서 원하는 구조를 찾지 못한 것이므로
                        // data 값을 반환
                        if (responseData.has("data")) {
                            return@withContext responseData.get("data").toString()
                        } else {
                            return@withContext responseData.toString()
                        }
                    } catch (e: Exception) {
                        // 파싱 과정에서 예외가 발생하면 data 값 반환
                        if (responseData.has("data")) {
                            return@withContext responseData.get("data").toString()
                        } else {
                            return@withContext responseData.toString()
                        }
                    }
                }
                is ApiResult.Error -> {
                    "요청 처리 중 오류가 발생했습니다: ${result.message}"
                }
            }
        } catch (e: Exception) {
            "요청 처리 중 오류가 발생했습니다: ${e.message ?: "알 수 없는 오류"}"
        }
    }
}