// CommentItem.kt
package com.android.hospitalAPP.ui.components

import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.*
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.unit.dp
import com.android.hospitalAPP.data.model.Comment

@Composable
fun CommentItem(
    comment: Comment,
    onReplyClick: (Int) -> Unit
) {
    Column(
        modifier = Modifier
            .fillMaxWidth()
            .padding(vertical = 4.dp)
    ) {
        // 사용자명 + 작성시간
        Row(
            verticalAlignment = Alignment.CenterVertically
        ) {
            Text(
                text = comment.username,
                style = MaterialTheme.typography.labelMedium
            )
            Spacer(Modifier.width(8.dp))
            Text(
                text = comment.createdAt,
                style = MaterialTheme.typography.bodySmall,
                color = Color.Gray
            )
        }

        Spacer(Modifier.height(2.dp))

        // 댓글 본문
        Text(
            text = comment.comment,
            style = MaterialTheme.typography.bodyLarge,
            modifier = Modifier.padding(start = 8.dp)
        )

        Spacer(Modifier.height(4.dp))

        // 답글 버튼
        Text(
            text = "답글 달기",
            style = MaterialTheme.typography.labelSmall.copy(color = MaterialTheme.colorScheme.primary),
            modifier = Modifier
                .padding(start = 8.dp)
                .clickable { onReplyClick(comment.id) }
        )
    }
}
