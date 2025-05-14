// ProfileManagementScreen.kt
package com.android.hospitalAPP.ui.screens

import androidx.compose.foundation.layout.*
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.foundation.text.KeyboardOptions
import androidx.compose.foundation.verticalScroll
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.ArrowBack
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.input.KeyboardType
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import androidx.lifecycle.viewmodel.compose.viewModel
import com.android.hospitalAPP.data.UserRepository
import com.android.hospitalAPP.navigation.Screen
import com.android.hospitalAPP.viewmodel.ProfileManagementViewModel
import java.text.SimpleDateFormat
import java.util.*

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun ProfileManagementScreen(
    onNavigateBack: () -> Unit,
    onNavigateChangePassword: () -> Unit,
    navigateToScreen: (String) -> Unit,
    onNavigateHome: () -> Unit,
    viewModel: ProfileManagementViewModel = viewModel()
) {
    val userRepository = UserRepository.getInstance()
    val currentUser by userRepository.currentUser.collectAsState()

    var userId by remember { mutableStateOf(currentUser?.userName ?: "") }
    val birthdateGMT = currentUser?.birthdate ?: ""
    var birthdate by remember { mutableStateOf(convertGmtToDateString(birthdateGMT)) }
    var email by remember { mutableStateOf(currentUser?.email ?: "") }
    var phone by remember { mutableStateOf(currentUser?.phone ?: "") }
    var address by remember { mutableStateOf(currentUser?.address ?: "") }
    var addressDetail by remember { mutableStateOf(currentUser?.address_detail ?: "") }

    // 1) ViewModel의 성공 플래그 구독
    val isEditSuccess by viewModel.isEditSuccess.collectAsState()
    val snackbarHostState = remember { SnackbarHostState() }

    // 2) 성공 시 스낵바 → 홈 이동 → 플래그 초기화
    LaunchedEffect(isEditSuccess) {
        if (isEditSuccess) {
            snackbarHostState.showSnackbar("회원정보가 수정되었습니다.")
            onNavigateHome()
            viewModel.clearEditSuccess()
        }
    }
    LaunchedEffect(currentUser) {
        if (currentUser == null) {
            navigateToScreen(Screen.Login.route)
        }
    }

    Scaffold(
        topBar = {
            TopAppBar(
                title = { Text("내 정보 관리") },
                navigationIcon = {
                    IconButton(onClick = onNavigateBack) {
                        Icon(Icons.Filled.ArrowBack, contentDescription = "뒤로가기")
                    }
                },
                colors = TopAppBarDefaults.topAppBarColors(containerColor = Color.White)
            )
        },
        snackbarHost = { SnackbarHost(snackbarHostState) }
    ) { paddingValues ->
        if (currentUser == null) {
            Box(
                modifier = Modifier
                    .fillMaxSize()
                    .padding(paddingValues),
                contentAlignment = Alignment.Center
            ) {
                Text("로그인이 필요한 서비스입니다.", fontSize = 18.sp)
            }
        } else {
            Column(
                modifier = Modifier
                    .fillMaxSize()
                    .padding(paddingValues)
                    .padding(16.dp)
                    .verticalScroll(rememberScrollState()),
                horizontalAlignment = Alignment.CenterHorizontally
            ) {
                // 프로필 헤더
                Box(
                    modifier = Modifier
                        .fillMaxWidth()
                        .padding(vertical = 24.dp),
                    contentAlignment = Alignment.Center
                ) {
                    Column(horizontalAlignment = Alignment.CenterHorizontally) {
                        Box(
                            modifier = Modifier
                                .size(80.dp)
                                .padding(8.dp),
                            contentAlignment = Alignment.Center
                        ) {
                            Text(
                                text = currentUser?.userName?.first().toString().uppercase(),
                                fontSize = 32.sp,
                                fontWeight = FontWeight.Bold,
                                color = Color(0xFF6650a4)
                            )
                        }
                        Spacer(Modifier.height(8.dp))
                        Text(currentUser?.userName ?: "", fontSize = 20.sp, fontWeight = FontWeight.Bold)
                    }
                }

                Divider()
                Spacer(Modifier.height(24.dp))

                // 읽기 전용 이름
                OutlinedTextField(
                    value = userId,
                    onValueChange = {},
                    label = { Text("이름") },
                    modifier = Modifier
                        .fillMaxWidth()
                        .padding(vertical = 8.dp),
                    shape = RoundedCornerShape(8.dp),
                    readOnly = true,
                    enabled = false
                )
                // 생일
                OutlinedTextField(
                    value = birthdate,
                    onValueChange = { birthdate = it },
                    label = { Text("생일") },
                    modifier = Modifier
                        .fillMaxWidth()
                        .padding(vertical = 8.dp),
                    shape = RoundedCornerShape(8.dp)
                )
                // 이메일
                OutlinedTextField(
                    value = email,
                    onValueChange = { email = it },
                    label = { Text("이메일") },
                    modifier = Modifier
                        .fillMaxWidth()
                        .padding(vertical = 8.dp),
                    shape = RoundedCornerShape(8.dp),
                    keyboardOptions = KeyboardOptions(keyboardType = KeyboardType.Email)
                )
                // 전화번호
                OutlinedTextField(
                    value = phone,
                    onValueChange = { phone = it },
                    label = { Text("전화번호") },
                    modifier = Modifier
                        .fillMaxWidth()
                        .padding(vertical = 8.dp),
                    shape = RoundedCornerShape(8.dp),
                    keyboardOptions = KeyboardOptions(keyboardType = KeyboardType.Phone)
                )
                // 주소
                OutlinedTextField(
                    value = address,
                    onValueChange = { address = it },
                    label = { Text("주소") },
                    modifier = Modifier
                        .fillMaxWidth()
                        .padding(vertical = 8.dp),
                    shape = RoundedCornerShape(8.dp)
                )
                // 상세주소
                OutlinedTextField(
                    value = addressDetail,
                    onValueChange = { addressDetail = it },
                    label = { Text("상세주소") },
                    modifier = Modifier
                        .fillMaxWidth()
                        .padding(vertical = 8.dp),
                    shape = RoundedCornerShape(8.dp)
                )

                Spacer(Modifier.height(24.dp))

                Button(
                    onClick = {
                        viewModel.update(
                            birthdate = birthdate,
                            email = email,
                            phone = phone,
                            address = address,
                            address_detail = addressDetail
                        )
                    },
                    modifier = Modifier
                        .fillMaxWidth()
                        .height(56.dp),
                    colors = ButtonDefaults.buttonColors(containerColor = Color(0xFFD0BCFF)),
                    shape = RoundedCornerShape(8.dp)
                ) {
                    Text("정보 수정", fontSize = 16.sp, color = Color.Black)
                }

                Spacer(Modifier.height(16.dp))

                OutlinedButton(
                    onClick = onNavigateChangePassword,
                    modifier = Modifier
                        .fillMaxWidth()
                        .height(56.dp),
                    shape = RoundedCornerShape(8.dp),
                    colors = ButtonDefaults.outlinedButtonColors(contentColor = Color(0xFF6650a4))
                ) {
                    Text("비밀번호 변경", fontSize = 16.sp)
                }

                Spacer(Modifier.height(40.dp))
            }
        }
    }
}

private fun convertGmtToDateString(gmtString: String): String {
    return try {
        val inputFormat = SimpleDateFormat("EEE, dd MMM yyyy HH:mm:ss z", Locale.ENGLISH)
        val outputFormat = SimpleDateFormat("yyyy-MM-dd", Locale.KOREA)
        val date = inputFormat.parse(gmtString) ?: return ""
        outputFormat.format(date)
    } catch (e: Exception) {
        e.printStackTrace()
        ""
    }
}
