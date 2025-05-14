// Comment.kt
package com.android.hospitalAPP.data.model

data class Comment(
    val id: Int,
    val qnaId: Int,
    val userId: Int,
    val username: String,
    val comment: String,
    val createdAt: String,
    val parentId: Int?,
    val replies: MutableList<Comment> = mutableListOf()
)