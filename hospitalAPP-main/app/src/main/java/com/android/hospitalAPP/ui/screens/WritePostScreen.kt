// WritePostScreen.kt
package com.android.hospitalAPP.ui.screens

import androidx.activity.compose.rememberLauncherForActivityResult
import androidx.activity.result.contract.ActivityResultContracts
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.foundation.verticalScroll
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.ArrowBack
import androidx.compose.material.icons.filled.Add
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import androidx.lifecycle.viewmodel.compose.viewModel
import com.android.hospitalAPP.viewmodel.CommunityViewModel
import com.android.hospitalAPP.data.UserRepository
import android.net.Uri

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun WritePostScreen(
    onNavigateBack: () -> Unit,
    onPostSuccess: () -> Unit,
    viewModel: CommunityViewModel = viewModel()
) {
    val userRepository = UserRepository.getInstance()
    val currentUser by userRepository.currentUser.collectAsState()
    val context = LocalContext.current

    // 파일 선택 관련 상태 추가
    var selectedImageUri by remember { mutableStateOf<Uri?>(null) }
    var selectedFileName by remember { mutableStateOf<String?>(null) }

    // 파일 선택 launcher - 이미지만 선택 가능하도록 설정
    val launcher = rememberLauncherForActivityResult(
        contract = ActivityResultContracts.GetContent()
    ) { uri: Uri? ->
        uri?.let {
            selectedImageUri = it

            // 파일명 추출
            context.contentResolver.query(it, null, null, null, null)?.use { cursor ->
                if (cursor.moveToFirst()) {
                    val displayNameIndex = cursor.getColumnIndex(android.provider.OpenableColumns.DISPLAY_NAME)
                    if (displayNameIndex != -1) {
                        selectedFileName = cursor.getString(displayNameIndex)
                    }
                }
            }
        }
    }

    if (currentUser == null) {
        // ✅ 로그인되지 않은 경우
        Scaffold(
            topBar = {
                TopAppBar(
                    title = { Text("글쓰기", fontWeight = FontWeight.Bold) },
                    navigationIcon = {
                        IconButton(onClick = onNavigateBack) {
                            Icon(
                                imageVector = Icons.Default.ArrowBack,
                                contentDescription = "뒤로가기"
                            )
                        }
                    },
                    colors = TopAppBarDefaults.topAppBarColors(
                        containerColor = Color.White
                    )
                )
            }
        ) { paddingValues ->
            Box(
                modifier = Modifier
                    .fillMaxSize()
                    .padding(paddingValues),
                contentAlignment = Alignment.Center
            ) {
                Text("로그인이 필요한 서비스입니다.")
            }
        }
        return
    }

    // ✅ 로그인된 경우
    var title by remember { mutableStateOf("") }
    var content by remember { mutableStateOf("") }
    // 카테고리 항상 "일반"으로 고정
    val defaultCategory = "일반"

    Scaffold(
        topBar = {
            TopAppBar(
                title = { Text("글쓰기", fontWeight = FontWeight.Bold) },
                navigationIcon = {
                    IconButton(onClick = onNavigateBack) {
                        Icon(
                            imageVector = Icons.Default.ArrowBack,
                            contentDescription = "뒤로가기"
                        )
                    }
                },
                actions = {
                    TextButton(
                        onClick = {
                            viewModel.addPost(title, content, defaultCategory, selectedImageUri, context)
                            onPostSuccess()
                        },
                        enabled = title.isNotBlank() && content.isNotBlank()
                    ) {
                        Text(
                            text = "등록",
                            color = if (title.isNotBlank() && content.isNotBlank())
                                Color(0xFFD0BCFF) else Color.Gray
                        )
                    }
                },
                colors = TopAppBarDefaults.topAppBarColors(
                    containerColor = Color.White
                )
            )
        }
    ) { paddingValues ->
        Column(
            modifier = Modifier
                .fillMaxSize()
                .padding(paddingValues)
                .padding(16.dp)
                .verticalScroll(rememberScrollState())
        ) {
            OutlinedTextField(
                value = title,
                onValueChange = { title = it },
                label = { Text("제목") },
                modifier = Modifier.fillMaxWidth(),
                shape = RoundedCornerShape(8.dp),
                colors = OutlinedTextFieldDefaults.colors(
                    focusedBorderColor = Color(0xFFD0BCFF),
                    unfocusedBorderColor = Color.LightGray
                )
            )

            Spacer(modifier = Modifier.height(16.dp))

            OutlinedTextField(
                value = content,
                onValueChange = { content = it },
                label = { Text("내용을 입력하세요") },
                modifier = Modifier
                    .fillMaxWidth()
                    .height(350.dp),
                shape = RoundedCornerShape(8.dp),
                colors = OutlinedTextFieldDefaults.colors(
                    focusedBorderColor = Color(0xFFD0BCFF),
                    unfocusedBorderColor = Color.LightGray
                )
            )

            Spacer(modifier = Modifier.height(16.dp))

            // 이미지 업로드 섹션
            Row(
                modifier = Modifier
                    .fillMaxWidth()
                    .padding(vertical = 8.dp),
                verticalAlignment = Alignment.CenterVertically
            ) {
                Button(
                    onClick = { launcher.launch("image/*") }, // 이미지 타입만 선택 가능하도록 설정
                    shape = RoundedCornerShape(8.dp),
                    colors = ButtonDefaults.buttonColors(
                        containerColor = Color(0xFFD0BCFF),
                        contentColor = Color.White
                    ),
                    contentPadding = PaddingValues(horizontal = 16.dp, vertical = 8.dp)
                ) {
                    Icon(
                        imageVector = Icons.Default.Add,
                        contentDescription = "이미지 첨부",
                        modifier = Modifier.size(20.dp)
                    )
                    Spacer(modifier = Modifier.width(4.dp))
                    Text("이미지 첨부")
                }

                Spacer(modifier = Modifier.width(8.dp))

                // 선택된 파일 이름 표시
                selectedFileName?.let {
                    Text(
                        text = it,
                        color = Color.Gray,
                        modifier = Modifier
                            .weight(1f)
                            .padding(start = 8.dp)
                    )
                }
            }

            // 선택된 파일이 있을 경우 취소 버튼 표시
            if (selectedFileName != null) {
                TextButton(
                    onClick = {
                        selectedImageUri = null
                        selectedFileName = null
                    },
                    modifier = Modifier.align(Alignment.End)
                ) {
                    Text("첨부 취소", color = Color.Gray)
                }
            }
        }
    }
}