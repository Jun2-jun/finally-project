// PostDetailScreen.kt
package com.android.hospitalAPP.ui.screens

import androidx.compose.foundation.layout.*
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items
import androidx.compose.material.Divider
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.ArrowBack
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import androidx.lifecycle.viewmodel.compose.viewModel
import com.android.hospitalAPP.data.model.Comment
import com.android.hospitalAPP.ui.components.CommentItem
import com.android.hospitalAPP.ui.components.ReplyItem
import com.android.hospitalAPP.viewmodel.CommunityViewModel

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun PostDetailScreen(
    postId: Int,
    onNavigateBack: () -> Unit,
    viewModel: CommunityViewModel = viewModel()
) {
    // 게시글 & 댓글 상태
    val posts by viewModel.posts.collectAsState()
    val post = posts.find { it.id == postId } ?: return
    val comments by viewModel.comments.collectAsState()

    // 입력 상태
    var newComment by remember { mutableStateOf("") }
    var replyingTo by remember { mutableStateOf<Int?>(null) }

    // 댓글 불러오기
    LaunchedEffect(postId) {
        viewModel.loadComments(postId)
    }

    Scaffold(
        topBar = {
            TopAppBar(
                title = { Text("게시글 상세") },
                navigationIcon = {
                    IconButton(onClick = onNavigateBack) {
                        Icon(Icons.Filled.ArrowBack, contentDescription = "뒤로가기")
                    }
                }
            )
        }
    ) { paddingValues ->
        LazyColumn(
            modifier = Modifier
                .padding(paddingValues)
                .padding(16.dp),
            verticalArrangement = Arrangement.spacedBy(12.dp)
        ) {
            // 1) 게시글 제목/작성자/좋아요/본문
            item {
                Text(
                    text = post.title,
                    fontSize = 22.sp,
                    fontWeight = FontWeight.Bold
                )
                Spacer(Modifier.height(8.dp))
                Divider()
                Spacer(Modifier.height(8.dp))
                Row(
                    horizontalArrangement = Arrangement.SpaceBetween,
                    modifier = Modifier.fillMaxWidth()
                ) {
                    Text("작성자: ${post.writer}", fontSize = 14.sp)
                    Text("좋아요: ${post.likes}", fontSize = 14.sp)
                }
                Spacer(Modifier.height(8.dp))
                Divider()
                Spacer(Modifier.height(16.dp))
                Text(text = post.content, fontSize = 16.sp)
            }

            // 2) 댓글 섹션 헤더
            item {
                Spacer(Modifier.height(24.dp))
                Text(text = "댓글", style = MaterialTheme.typography.titleMedium)
            }

            // 3) 댓글 & 대댓글 리스트
            items(comments) { comment ->
                // 일반 댓글
                CommentItem(
                    comment = comment,
                    onReplyClick = { replyingTo = comment.id }
                )

                // 대댓글
                comment.replies.forEach { reply ->
                    ReplyItem(
                        reply = reply,
                        modifier = Modifier
                            .fillMaxWidth()
                            .padding(start = 24.dp, top = 4.dp, bottom = 4.dp)
                    )
                    // 대댓글마다 구분선도 들여쓰기
                    Divider(modifier = Modifier.padding(start = 24.dp))
                }

                // 댓글 간 구분선
                Divider()
            }
            // 4) 입력창
            item {
                Spacer(Modifier.height(16.dp))
                Row(
                    modifier = Modifier
                        .fillMaxWidth()
                        .padding(vertical = 8.dp),
                    verticalAlignment = Alignment.CenterVertically
                ) {
                    OutlinedTextField(
                        value = newComment,
                        onValueChange = { newComment = it },
                        label = {
                            Text(if (replyingTo == null) "댓글 입력" else "대댓글 입력")
                        },
                        modifier = Modifier.weight(1f)
                    )
                    Spacer(Modifier.width(8.dp))
                    Button(onClick = {
                        if (newComment.isNotBlank()) {
                            viewModel.postComment(postId, newComment.trim(), replyingTo)
                            newComment = ""
                            replyingTo = null
                        }
                    }) {
                        Text("등록")
                    }
                }
            }
        }
    }
}
