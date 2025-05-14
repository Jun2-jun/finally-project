// PostRepository.kt - API 통신을 위해 수정됨
package com.android.hospitalAPP.data

import android.content.Context
import android.net.Uri
import com.android.hospitalAPP.viewmodel.CommunityViewModel.Post
import com.android.hospitalAPP.viewmodel.CommunityViewModel.Notice
import kotlinx.coroutines.CoroutineScope
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.launch
import kotlinx.coroutines.withContext
import org.json.JSONObject
import java.text.SimpleDateFormat
import java.util.*
import android.util.Log
import org.json.JSONArray
import okhttp3.MultipartBody
import okhttp3.MediaType.Companion.toMediaTypeOrNull
import okhttp3.RequestBody.Companion.asRequestBody
import okhttp3.Request
import java.io.File
import java.io.FileOutputStream

// ✅ 게시글 및 공지사항 관리 리포지토리 (API 연동)
object PostRepository {
    // 게시글 목록 상태 저장
    private val _posts = MutableStateFlow<List<Post>>(emptyList())
    val posts: StateFlow<List<Post>> = _posts

    // 공지사항 목록 상태 저장
    private val _notices = MutableStateFlow<List<Notice>>(emptyList())
    val notices: StateFlow<List<Notice>> = _notices

    // API 통신을 위한 CoroutineScope
    private val coroutineScope = CoroutineScope(Dispatchers.IO)
    private val postService = PostService()

    init {
        // 앱 시작 시 게시글 불러오기
        fetchPosts()
    }

    /**
     * ✅ 서버에서 게시글 목록 불러오기 (QnA 데이터)
     */
    fun fetchPosts() {
        coroutineScope.launch(Dispatchers.IO) {
            try {
                Log.d("PostRepository", "QnA 데이터 요청 시작")

                when (val result = postService.getPosts()) {
                    is ApiResult.Success -> {
                        val jsonArray = result.data
                        Log.d("PostRepository", "QnA 데이터 수신: ${jsonArray.length()}개")

                        if (jsonArray.length() > 0) {
                            Log.d("PostRepository", "첫 번째 항목: ${jsonArray.getJSONObject(0)}")
                        }

                        val postList = mutableListOf<Post>()
                        for (i in 0 until jsonArray.length()) {
                            try {
                                val item = jsonArray.getJSONObject(i)
                                val post = Post(
                                    id = item.getInt("id"),
                                    title = item.optString("title", ""),
                                    content = item.optString("comment", ""), // comment 필드 사용
                                    writer = item.optString("writer", "writer"),
                                    timeAgo = calculateTimeAgo(item.optString("created_at", "")),
                                    likes = item.optInt("likes", 0),
                                    comments = item.optInt("comments", 0)
                                )
                                postList.add(post)
                            } catch (e: Exception) {
                                Log.e("PostRepository", "QnA 항목 파싱 오류: ${e.message}")
                                continue
                            }
                        }

                        Log.d("PostRepository", "QnA 파싱 완료: ${postList.size}개")
                        _posts.value = postList
                    }

                    is ApiResult.Error -> {
                        Log.e("PostRepository", "QnA 요청 실패: ${result.message}")
                    }
                }
            } catch (e: Exception) {
                Log.e("PostRepository", "QnA 처리 중 예외 발생: ${e.message}")
            }
        }
    }

    /**
     * ✅ 게시글 목록 API 요청 (QnA용)
     */
    private suspend fun getPostsFromApi(page: Int = 1, perPage: Int = 20): ApiResult<JSONArray> = withContext(Dispatchers.IO) {
        try {
            val url = "${ApiConstants.POSTS_URL}?page=$page&per_page=$perPage"
            val result = ApiServiceCommon.getRequest(url)

            return@withContext when (result) {
                is ApiResult.Success -> {
                    try {
                        val jsonObject = result.data as? JSONObject
                        val dataObject = jsonObject?.optJSONObject("data")
                        val dataArray = dataObject?.optJSONArray("items") ?: JSONArray()
                        ApiResult.Success(dataArray)
                    } catch (e: Exception) {
                        Log.e("PostService", "QnA JSON 파싱 오류: ${e.message}")
                        ApiResult.Error(message = "QnA 데이터 파싱 오류: ${e.message}")
                    }
                }

                is ApiResult.Error -> {
                    ApiResult.Error(message = result.message)
                }
            }
        } catch (e: Exception) {
            Log.e("PostService", "QnA 요청 처리 중 예외 발생: ${e.message}")
            ApiResult.Error(message = "요청 처리 중 오류가 발생했습니다: ${e.message}")
        }
    }

    /**
     * ✅ JSON 객체를 Post 객체로 변환
     */
    private fun parsePostFromJson(postJson: JSONObject): Post {
        val id = postJson.getInt("id")
        val title = postJson.optString("title", "")
        val content = postJson.optString("comment", "")  // API는 comment 필드 사용
        val writer = postJson.optString("writer","writer")
        val createdAt = postJson.optString("created_at", "")
        val likes = postJson.optInt("likes", 0)
        val comments = postJson.optInt("comments", 0)

        // 작성 시간 가공
        val timeAgo = calculateTimeAgo(createdAt)

        return Post(
            id = id,
            title = title,
            content = content,
            writer = writer,
            timeAgo = timeAgo,
            likes = likes,
            comments = comments
        )
    }

    /**
     * ✅ 작성 시각을 '방금 전', 'n시간 전' 형식으로 변환
     */
    fun calculateTimeAgo(createdAt: String): String {
        return try {
            val formatter = SimpleDateFormat("yyyy-MM-dd HH:mm:ss", Locale.getDefault())
            val createdDate = formatter.parse(createdAt)
            if (createdDate != null) {
                val currentTime = Date().time
                val timeDiff = currentTime - createdDate.time
                val minutes = timeDiff / (1000 * 60)

                when {
                    minutes < 1 -> "방금 전"
                    minutes < 60 -> "${minutes}분 전"
                    minutes < 60 * 24 -> "${minutes / 60}시간 전"
                    else -> "${minutes / 60 / 24}일 전"
                }
            } else {
                "날짜 오류"
            }
        } catch (e: Exception) {
            Log.e("DateParseError", "날짜 파싱 실패: $createdAt", e)
            "날짜 오류"
        }
    }

    /**
     * ✅ 게시글 추가 (API 연동)
     */
    fun addPost(title: String, content: String, category: String, fileUri: Uri?, context: Context) {
        coroutineScope.launch {
            try {
                val result = createPostApi(title, content, category, fileUri, context)

                if (result is ApiResult.Success) {
                    val jsonResponse = result.data
                    val status = jsonResponse.optString("status")

                    if (status == "success") {
                        fetchPosts()
                    } else {
                        println("게시글 추가 실패: ${jsonResponse.optString("message", "알 수 없는 오류")}")
                        addPostLocally(title, content, category)
                    }
                } else if (result is ApiResult.Error) {
                    println("게시글 추가 요청 실패: ${result.message}")
                    addPostLocally(title, content, category)
                }
            } catch (e: Exception) {
                println("게시글 추가 중 예외 발생: ${e.message}")
                addPostLocally(title, content, category)
            }
        }
    }

    /**
     * ✅ 게시글 추가 API 요청 (POST)
     */
    private suspend fun createPostApi(title: String, content: String, category: String, fileUri: Uri?, context: Context): ApiResult<JSONObject> = withContext(Dispatchers.IO) {
        try {
            val jsonBody = JSONObject().apply {
                put("title", title)
                put("comment", content)
                put("category", category) // 서버 코드에서 사용하는 필드명
            }

            if (fileUri != null) {
                // 이미지 파일이 있는 경우, MultipartBody 사용
                val requestBody = MultipartBody.Builder()
                    .setType(MultipartBody.FORM)

                // 파일명 추출
                val fileName = getFileNameFromUri(context, fileUri) ?: "image.jpg"
                val tempFile = createTempFileFromUri(context, fileUri, fileName)

                if (tempFile != null) {
                    // 서버 코드에 맞게 필드명을 'images'로 변경
                    requestBody.addFormDataPart(
                        "images",
                        fileName,
                        tempFile.asRequestBody(getMimeType(fileName).toMediaTypeOrNull())
                    )

                    // JSON 데이터의 각 필드를 form data로 추가
                    requestBody.addFormDataPart("title", title)
                        .addFormDataPart("comment", content)
                        .addFormDataPart("category", category)

                    val sessionId = UserRepository.getInstance().getSessionId()

                    val request = Request.Builder()
                        .url(ApiConstants.POSTS_URL)
                        .post(requestBody.build())
                        .addHeader("Cookie", "session=$sessionId")
                        .addHeader("Connection", "close")
                        .build()

                    return@withContext ApiServiceCommon.executeMultipartRequest(request, tempFile)
                } else {
                    // 파일 생성 실패 시 일반 JSON 요청으로 전환
                    return@withContext ApiServiceCommon.postRequest(ApiConstants.POSTS_URL, jsonBody)
                }
            } else {
                // 파일이 없는 경우 일반 JSON 요청
                return@withContext ApiServiceCommon.postRequest(ApiConstants.POSTS_URL, jsonBody)
            }
        } catch (e: Exception) {
            Log.e("PostRepository", "게시글 생성 API 요청 중 오류: ${e.message}", e)
            return@withContext ApiResult.Error(message = "게시글 생성 요청 실패: ${e.message}")
        }
    }

    /**
     * ✅ API 실패 시, 로컬에 임시로 게시글 추가
     */
    private fun addPostLocally(title: String, content: String, writer: String) {
        val userRepository = UserRepository.getInstance()
        val currentUser = userRepository.currentUser.value

        val username = currentUser?.userName ?: "익명" // 로그인되지 않은 경우 "익명"으로 표시

        val newId = System.currentTimeMillis().toInt()
        val newPost = Post(
            id = newId,
            title = title,
            content = content,// 실제 사용자 이름 사용
            writer = username,
            timeAgo = "방금 전",
            likes = 0,
            comments = 0
        )

        val currentPosts = _posts.value.toMutableList()
        currentPosts.add(0, newPost)
        _posts.value = currentPosts
    }

    // Uri에서 파일명 추출
    private fun getFileNameFromUri(context: Context, uri: Uri): String? {
        val cursor = context.contentResolver.query(uri, null, null, null, null)
        return cursor?.use {
            if (it.moveToFirst()) {
                val displayNameIndex = it.getColumnIndex(android.provider.OpenableColumns.DISPLAY_NAME)
                if (displayNameIndex != -1) {
                    it.getString(displayNameIndex)
                } else null
            } else null
        }
    }

    // Uri에서 임시 파일 생성
    private fun createTempFileFromUri(context: Context, uri: Uri, fileName: String): File? {
        return try {
            val tempFile = File(context.cacheDir, fileName)
            context.contentResolver.openInputStream(uri)?.use { inputStream ->
                FileOutputStream(tempFile).use { outputStream ->
                    inputStream.copyTo(outputStream)
                }
            }
            tempFile
        } catch (e: Exception) {
            Log.e("PostRepository", "임시 파일 생성 실패: ${e.message}", e)
            null
        }
    }

    // 파일 확장자로 MIME 타입 추정
    private fun getMimeType(fileName: String): String {
        return when {
            fileName.endsWith(".jpg", true) || fileName.endsWith(".jpeg", true) -> "image/jpeg"
            fileName.endsWith(".png", true) -> "image/png"
            fileName.endsWith(".gif", true) -> "image/gif"
            fileName.endsWith(".bmp", true) -> "image/bmp"
            fileName.endsWith(".webp", true) -> "image/webp"
            else -> "image/jpeg" // 기본 타입을 이미지로 설정
        }
    }
}


class PostService {
    suspend fun getPosts(): ApiResult<JSONArray> = withContext(Dispatchers.IO) {
        try {
            val url = ApiConstants.POSTS_URL
            val result = ApiServiceCommon.getRequest(url)

            return@withContext when (result) {
                is ApiResult.Success -> {
                    try {
                        val jsonObject = result.data as? JSONObject
                        val dataObject = jsonObject?.optJSONObject("data")
                        val dataArray = dataObject?.optJSONArray("items") ?: JSONArray()
                        ApiResult.Success(dataArray)
                    } catch (e: Exception) {
                        Log.e("PostService", "QnA JSON 파싱 오류: ${e.message}")
                        ApiResult.Error(message = "QnA 데이터 파싱 오류: ${e.message}")
                    }
                }
                is ApiResult.Error -> {
                    ApiResult.Error(message = result.message)
                }
            }
        } catch (e: Exception) {
            Log.e("PostService", "QnA 요청 처리 중 예외 발생: ${e.message}")
            ApiResult.Error(message = "요청 처리 중 오류가 발생했습니다: ${e.message}")
        }
    }
}