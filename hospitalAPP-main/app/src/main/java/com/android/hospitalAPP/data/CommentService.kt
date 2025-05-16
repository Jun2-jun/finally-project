// CommentService.kt
package com.android.hospitalAPP.data

import com.android.hospitalAPP.data.ApiServiceCommon
import com.android.hospitalAPP.data.ApiConstants
import com.android.hospitalAPP.data.model.Comment
import okhttp3.FormBody
import org.json.JSONObject
import android.util.Log
import org.json.JSONArray
import org.json.JSONTokener




object CommentService {

    /** Q&A 댓글 불러오기 */
    suspend fun getComments(qnaId: Int): List<Comment> {
        val response = ApiServiceCommon.getRequest("${ApiConstants.POSTS_URL}$qnaId/comments")
        // 성공 케이스면 JSONObject.toString(), 아니면 빈 문자열
        val raw = (response as? ApiResult.Success)?.data?.toString() ?: ""

        return try {
            when (val parsed = JSONTokener(raw).nextValue()) {
                is JSONObject -> {
                    // 기존 { data: { items: [...] } } 구조
                    val items = parsed.getJSONObject("data").getJSONArray("items")
                    parseComments(items, qnaId)
                }
                is JSONArray -> {
                    // [ { comment:..., replies:[...] }, … ] 구조
                    parseComments(parsed, qnaId)
                }
                else -> emptyList()
            }
        } catch (e: Exception) {
            emptyList()
        }
    }

    /** JSON 배열을 넘기면, 각 요소의 replies 키까지 읽어서 Comment.replies 에 담아 줍니다. */
    private fun parseComments(arr: JSONArray, qnaId: Int): List<Comment> {
        val list = mutableListOf<Comment>()
        for (i in 0 until arr.length()) {
            val o = arr.getJSONObject(i)
            // 1) 먼저 최상위 댓글
            val parent = Comment(
                id        = o.getInt("id"),
                qnaId     = qnaId,
                userId    = o.optInt("user_id"),      // Q&A API 에 user_id 가 없으면 optString 써야 할 수도 있어요
                username  = o.getString("username"),
                comment   = o.getString("comment"),
                createdAt = o.getString("created_at"),
                parentId  = o.optInt("parent_id").takeIf { it != 0 },
                replies   = mutableListOf()            // 아직 비워 두고…
            )
            // 2) nested replies 파싱
            val repliesJson = o.optJSONArray("replies") ?: JSONArray()
            val repliesList = mutableListOf<Comment>()
            for (j in 0 until repliesJson.length()) {
                val ro = repliesJson.getJSONObject(j)
                repliesList += Comment(
                    id        = ro.getInt("id"),
                    qnaId     = qnaId,
                    userId    = ro.optInt("user_id"),
                    username  = ro.getString("username"),
                    comment   = ro.getString("comment"),
                    createdAt = ro.getString("created_at"),
                    parentId  = ro.optInt("parent_id").takeIf { it != 0 },
                    replies   = mutableListOf()          // 대댓글의 대댓글은 아직 없으니 빈 리스트
                )
            }
            // 3) 최상위 댓글에 대댓글 리스트 연결
            list += parent.copy(replies = repliesList)
        }
        return list
    }



    /** Q&A 댓글 / 대댓글 등록 */
    suspend fun postComment(
        qnaId: Int,
        text: String,
        parentId: Int? = null
    ): Boolean {
        val url = "${ApiConstants.POSTS_URL}$qnaId/comments"
        val formBody = FormBody.Builder()
            .add("comment", text)
            .apply { parentId?.let { add("parent_id", it.toString()) } }
            .build()

        return when (ApiServiceCommon.postForm(url, formBody)) {
            is ApiResult.Success<*> -> true
            else                   -> false
        }
    }

    /** 서버가 내려주는 JSON을 Comment 모델 리스트로 변환 */
    private fun parseComments(json: JSONObject, qnaId: Int): List<Comment> {
        val flat = mutableListOf<Comment>()
        val arr = json.optJSONArray("comments") ?: return emptyList()
        for (i in 0 until arr.length()) {
            arr.optJSONObject(i)?.let { o ->
                flat += Comment(
                    id        = o.optInt("id"),
                    qnaId     = qnaId,
                    userId    = o.optInt("user_id"),//이거없엉
                    username  = o.optString("username"),
                    comment   = o.optString("comment"),
                    createdAt = o.optString("created_at"),
                    parentId  = o.optInt("parent_id").takeIf { it != 0 }
                    // replies 프로퍼티는 나중에 채워줄 거니까 디폴트(빈 MutableList)로 놔둡니다.
                )
            }
        }
        val byParent = flat.groupBy { it.parentId }
        return byParent[null]?.map { parent ->
            parent.copy(
                replies = (byParent[parent.id] ?: emptyList())
                    .toMutableList()   // ← List → MutableList 변환!
            )
        } ?: emptyList()
    }
}
