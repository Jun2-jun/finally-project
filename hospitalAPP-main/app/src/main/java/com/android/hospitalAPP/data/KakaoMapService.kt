// KakaoMapService.kt
package com.android.hospitalAPP.data

import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.withContext
import okhttp3.HttpUrl.Companion.toHttpUrl
import okhttp3.OkHttpClient
import okhttp3.Request
import org.json.JSONObject
import java.io.IOException

/**
 * 카카오 지도 API 서비스
 */
class KakaoMapService {
    private val client = OkHttpClient()

    // 카카오맵 REST API 키 (실제 키로 교체 필요)
    private val REST_API_KEY = "27d042f646cee0fe06d489dd31e0c4b0"

    // 카카오맵 검색 API 기본 URL
    private val KAKAO_SEARCH_API_URL = "https://dapi.kakao.com/v2/local/search/keyword.json"

    /**
     * 키워드로 장소 검색
     * @param keyword 검색 키워드
     * @param x 중심 경도 좌표 (기준점)
     * @param y 중심 위도 좌표 (기준점)
     * @param radius 반경 (미터)
     * @return 검색 결과 리스트
     */
    suspend fun searchPlaces(
        keyword: String,
        x: Double? = null,
        y: Double? = null,
        radius: Int = 2000
    ): Result<List<PlaceSearchResult>> = withContext(Dispatchers.IO) {
        try {
            // URL 생성 및 검색 파라미터 추가
            val urlBuilder = KAKAO_SEARCH_API_URL.toHttpUrl().newBuilder()
                .addQueryParameter("query", keyword)
                .addQueryParameter("page", "1")
                .addQueryParameter("size", "15")

            // 좌표가 있으면 반경 검색 적용
            if (x != null && y != null) {
                urlBuilder.addQueryParameter("x", x.toString())
                    .addQueryParameter("y", y.toString())
                    .addQueryParameter("radius", radius.toString())
                    .addQueryParameter("sort", "distance") // 거리순 정렬
            }

            val url = urlBuilder.build()

            // API 요청 객체 생성
            val request = Request.Builder()
                .url(url)
                .addHeader("Authorization", "KakaoAK $REST_API_KEY")
                .build()

            // API 호출 실행
            client.newCall(request).execute().use { response ->
                if (!response.isSuccessful) {
                    return@withContext Result.failure(IOException("API 호출 실패: ${response.code}"))
                }

                val responseBody = response.body?.string() ?: return@withContext Result.failure(IOException("응답 데이터 없음"))
                val jsonResponse = JSONObject(responseBody)

                // JSON 파싱 및 결과 매핑
                val documents = jsonResponse.getJSONArray("documents")
                val results = mutableListOf<PlaceSearchResult>()

                for (i in 0 until documents.length()) {
                    val item = documents.getJSONObject(i)
                    results.add(
                        PlaceSearchResult(
                            id = item.getString("id"),
                            name = item.getString("place_name"),
                            address = item.getString("road_address_name").ifEmpty { item.getString("address_name") },
                            phone = item.getString("phone"),
                            distance = calculateDistance(item.getString("distance")),
                            latitude = item.getString("y").toDouble(),
                            longitude = item.getString("x").toDouble()
                        )
                    )
                }

                Result.success(results)
            }
        } catch (e: Exception) {
            Result.failure(e)
        }
    }

    /**
     * 거리 문자열 형식화
     * @param distanceStr API로부터 받은 거리 문자열 (미터 단위)
     * @return 형식화된 거리 문자열 (1km 이상은 km 단위, 미만은 m 단위)
     */
    private fun calculateDistance(distanceStr: String): String {
        return try {
            val distance = distanceStr.toInt()
            if (distance >= 1000) {
                String.format("%.1fkm", distance / 1000.0)
            } else {
                "${distance}m"
            }
        } catch (e: Exception) {
            distanceStr
        }
    }
}

/**
 * 장소 검색 결과 데이터 클래스
 */
data class PlaceSearchResult(
    val id: String,
    val name: String,
    val address: String,
    val phone: String,
    val distance: String,
    val latitude: Double,
    val longitude: Double
)