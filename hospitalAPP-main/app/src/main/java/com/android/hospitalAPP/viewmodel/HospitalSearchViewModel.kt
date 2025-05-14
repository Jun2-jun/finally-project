// HospitalSearchViewModel.kt
package com.android.hospitalAPP.viewmodel

import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import com.android.hospitalAPP.data.KakaoMapService
import com.android.hospitalAPP.data.PlaceSearchResult
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.launch

class HospitalSearchViewModel : ViewModel() {
    private val kakaoMapService = KakaoMapService()

    // 검색 결과를 관리하는 StateFlow
    private val _searchResults = MutableStateFlow<List<PlaceSearchResult>>(emptyList())
    val searchResults: StateFlow<List<PlaceSearchResult>> = _searchResults

    // 선택된 장소를 관리하는 StateFlow
    private val _selectedPlace = MutableStateFlow<PlaceSearchResult?>(null)
    val selectedPlace: StateFlow<PlaceSearchResult?> = _selectedPlace

    // 로딩 상태
    private val _isLoading = MutableStateFlow(false)
    val isLoading: StateFlow<Boolean> = _isLoading

    // 에러 메시지
    private val _errorMessage = MutableStateFlow<String?>(null)
    val errorMessage: StateFlow<String?> = _errorMessage

    // 마지막 검색 키워드
    private val _lastQuery = MutableStateFlow("")
    val lastQuery: StateFlow<String> = _lastQuery

    /**
     * 키워드로 병원 검색 수행
     * @param query 검색 키워드
     * @param x 중심 경도 좌표 (현재 위치)
     * @param y 중심 위도 좌표 (현재 위치)
     */
    fun searchHospitals(query: String, x: Double? = null, y: Double? = null) {
        if (query.isBlank()) return

        _lastQuery.value = query
        _isLoading.value = true
        _errorMessage.value = null

        viewModelScope.launch {
            try {
                // 카카오맵 API 호출
                val searchQuery = if (!query.contains("병원") && !query.endsWith("과")) {
                    "$query 병원" // '병원' 키워드 자동 추가
                } else {
                    query
                }

                val result = kakaoMapService.searchPlaces(searchQuery, x, y)

                result.fold(
                    onSuccess = { places ->
                        _searchResults.value = places
                        // 첫 번째 항목 자동 선택
                        _selectedPlace.value = places.firstOrNull()
                        _isLoading.value = false
                    },
                    onFailure = { error ->
                        _errorMessage.value = "검색 중 오류가 발생했습니다: ${error.message}"
                        _isLoading.value = false
                    }
                )
            } catch (e: Exception) {
                _errorMessage.value = "검색 중 오류가 발생했습니다: ${e.message}"
                _isLoading.value = false
            }
        }
    }

    /**
     * 장소 선택
     * @param place 선택한 장소
     */
    fun selectPlace(place: PlaceSearchResult) {
        _selectedPlace.value = place
    }

    /**
     * 에러 메시지 초기화
     */
    fun clearError() {
        _errorMessage.value = null
    }
}