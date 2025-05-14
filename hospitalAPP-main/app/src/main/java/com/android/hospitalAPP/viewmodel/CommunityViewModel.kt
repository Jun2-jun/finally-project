package com.android.hospitalAPP.viewmodel

import android.content.Context
import android.net.Uri
import android.util.Log
import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import com.android.hospitalAPP.data.ApiResult
import com.android.hospitalAPP.data.CommentService
import com.android.hospitalAPP.data.PostRepository
import com.android.hospitalAPP.data.PostRepository.fetchPosts
import com.android.hospitalAPP.data.model.Comment
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.launch
import kotlinx.coroutines.withContext
import org.json.JSONArray
import com.android.hospitalAPP.data.ApiServiceCommon
import com.android.hospitalAPP.data.ApiConstants


class CommunityViewModel : ViewModel() {

    // 게시글 흐름 (PostRepository 내부에서 fetchPosts() 호출)
    val posts: StateFlow<List<Post>> = PostRepository.posts

    // 공지사항 흐름
    private val _notices = MutableStateFlow<List<Notice>>(emptyList())
    val notices: StateFlow<List<Notice>> = _notices
    private val noticeService = NoticeService()

    init {
        // 초기 로드
        fetchNotices()
        fetchPosts()
    }

    // 댓글 흐름
    private val _comments = MutableStateFlow<List<Comment>>(emptyList())
    val comments: StateFlow<List<Comment>> = _comments

    /** 특정 Q&A 글의 댓글/대댓글을 불러옵니다. */
    fun loadComments(qnaId: Int) {
        viewModelScope.launch(Dispatchers.IO) {
            _comments.value = CommentService.getComments(qnaId)
        }
    }

    /** 댓글 또는 대댓글을 등록하고, 성공 시 댓글 리스트를 다시 불러옵니다. */
    fun postComment(qnaId: Int, text: String, parentId: Int? = null) {
        viewModelScope.launch(Dispatchers.IO) {
            if (CommentService.postComment(qnaId, text, parentId)) {
                loadComments(qnaId)
            }
        }
    }

    /** 공지사항 데이터 요청 */
    private fun fetchNotices() {
        viewModelScope.launch(Dispatchers.IO) {
            try {
                Log.d("CommunityViewModel", "공지사항 데이터 요청 시작")
                when (val result = noticeService.getNotices()) {
                    is ApiResult.Success -> {
                        val jsonArray = result.data
                        Log.d("CommunityViewModel", "공지사항 데이터 수신: ${jsonArray.length()}개")

                        val noticeList = mutableListOf<Notice>()
                        for (i in 0 until jsonArray.length()) {
                            try {
                                val item = jsonArray.getJSONObject(i)
                                noticeList += Notice(
                                    id = item.getInt("id"),
                                    title = item.getString("title"),
                                    comment = item.getString("comment"),
                                    image_urls = item.optString("image_urls", null),
                                    created_at = item.getString("created_at"),
                                    views = item.optInt("views", 0),
                                    user_id = item.optInt("user_id").takeIf { !item.isNull("user_id") }
                                )
                            } catch (e: Exception) {
                                Log.e("CommunityViewModel", "공지사항 항목 파싱 오류: ${e.message}")
                            }
                        }

                        _notices.value = noticeList
                        Log.d("CommunityViewModel", "공지사항 파싱 완료: ${noticeList.size}개")
                    }
                    is ApiResult.Error -> {
                        Log.e("CommunityViewModel", "공지사항 요청 실패: ${result.message}")
                    }
                }
            } catch (e: Exception) {
                Log.e("CommunityViewModel", "공지사항 처리 중 예외 발생: ${e.message}")
            }
        }
    }

    /** 새 게시글 등록 */
    fun addPost(title: String, content: String, category: String, fileUri: Uri?, context: Context) {
        PostRepository.addPost(title, content, category, fileUri, context)
    }

    // 데이터 클래스 정의
    data class Post(
        val id: Int,
        val title: String,
        val content: String,
        val writer: String,
        val timeAgo: String,
        val likes: Int,
        val comments: Int
    )

    data class Notice(
        val id: Int,
        val title: String,
        val comment: String,
        val image_urls: String?,
        val created_at: String,
        val views: Int,
        val user_id: Int?
    )

    /** 내부 클래스: 공지사항 API 호출 & JSON 파싱 */
    inner class NoticeService {
        suspend fun getNotices(): ApiResult<JSONArray> = withContext(Dispatchers.IO) {
            // 1) API 호출
            val result = ApiServiceCommon.getRequest(ApiConstants.NOTICES_URL)

            // 2) 결과 처리
            when (result) {
                is ApiResult.Success -> {
                    try {
                        // { "data": { "items": [ ... ] } } 구조에서 items 배열만 뽑아냄
                        val dataObj = result.data.optJSONObject("data")
                        val items = dataObj?.optJSONArray("items") ?: JSONArray()
                        ApiResult.Success(items)
                    } catch (e: Exception) {
                        Log.e("NoticeService", "JSON 파싱 오류: ${e.message}", e)
                        ApiResult.Error(message = "데이터 파싱 중 오류: ${e.message}")
                    }
                }
                is ApiResult.Error -> {
                    // 에러면 그대로 전달
                    ApiResult.Error(code = result.code, message = result.message)
                }
            }
        }
    }
}