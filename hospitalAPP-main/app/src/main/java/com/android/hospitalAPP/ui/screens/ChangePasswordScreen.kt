// ChangePasswordScreen.kt
package com.android.hospitalAPP.ui.screens

import androidx.compose.foundation.layout.*
import androidx.compose.foundation.rememberScrollState
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
import androidx.compose.ui.text.input.PasswordVisualTransformation
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import kotlinx.coroutines.launch
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.lifecycle.viewmodel.compose.viewModel
import com.android.hospitalAPP.viewmodel.ChangePasswordViewModel


@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun ChangePasswordScreen(
    onNavigateBack: () -> Unit,
    onPasswordChanged: () -> Unit,
    viewModel: ChangePasswordViewModel = viewModel()
) {
    val snackbarHostState = remember { SnackbarHostState() }
    val scope = rememberCoroutineScope()

    var current_password by remember { mutableStateOf("") }
    var new_password by remember { mutableStateOf("") }
    var confirmPassword by remember { mutableStateOf("") }
    var isLoading by remember { mutableStateOf(false) }

    var email by remember { mutableStateOf("") }
    var emailCode by remember { mutableStateOf("") }
    var isEmailVerified by remember { mutableStateOf(false) }

    LaunchedEffect(Unit) {
        // 필요 시 초기화 로직
    }

    Scaffold(
        topBar = {
            TopAppBar(
                title = { Text("비밀번호 변경") },
                navigationIcon = {
                    IconButton(onClick = onNavigateBack) {
                        Icon(Icons.Filled.ArrowBack, contentDescription = "뒤로가기")
                    }
                },
                colors = TopAppBarDefaults.topAppBarColors(containerColor = Color.White)
            )
        },
        snackbarHost = { SnackbarHost(hostState = snackbarHostState) }
    ) { paddingValues ->
        Column(
            modifier = Modifier
                .fillMaxSize()
                .padding(paddingValues)
                .padding(16.dp)
                .verticalScroll(rememberScrollState()),
            horizontalAlignment = Alignment.CenterHorizontally
        ) {
            OutlinedTextField(
                value = current_password,
                onValueChange = { current_password = it },
                label = { Text("현재 비밀번호") },
                modifier = Modifier
                    .fillMaxWidth()
                    .padding(vertical = 8.dp),
                visualTransformation = PasswordVisualTransformation(),
                keyboardOptions = KeyboardOptions(keyboardType = KeyboardType.Password),
                singleLine = true
            )

            OutlinedTextField(
                value = new_password,
                onValueChange = { new_password = it },
                label = { Text("새 비밀번호") },
                modifier = Modifier
                    .fillMaxWidth()
                    .padding(vertical = 8.dp),
                visualTransformation = PasswordVisualTransformation(),
                keyboardOptions = KeyboardOptions(keyboardType = KeyboardType.Password),
                singleLine = true
            )

            OutlinedTextField(
                value = confirmPassword,
                onValueChange = { confirmPassword = it },
                label = { Text("새 비밀번호 확인") },
                modifier = Modifier
                    .fillMaxWidth()
                    .padding(vertical = 8.dp),
                visualTransformation = PasswordVisualTransformation(),
                keyboardOptions = KeyboardOptions(keyboardType = KeyboardType.Password),
                singleLine = true
            )

            // 이메일 입력
            OutlinedTextField(
                value = email,
                onValueChange = { email = it },
                label = { Text("이메일") },
                modifier = Modifier
                    .fillMaxWidth()
                    .padding(vertical = 8.dp),
                keyboardOptions = KeyboardOptions(keyboardType = KeyboardType.Email),
                singleLine = true
            )

            // 인증코드 발송 버튼
            Button(
                onClick = {
                    if (!isValidEmail(email)) {
                        scope.launch {
                            snackbarHostState.showSnackbar("올바른 이메일 형식을 입력해주세요.")
                        }
                    } else {
                        // 이메일 형식이 올바르면 API 요청
                        scope.launch {
                            // TODO: 이메일 인증코드 전송 API 호출
                            viewModel.sendEmailCode(email)
                            snackbarHostState.showSnackbar("인증 코드가 이메일로 전송되었습니다.")
                        }
                    }
                },
                modifier = Modifier
                    .align(Alignment.End)
                    .padding(bottom = 8.dp),
                colors = ButtonDefaults.buttonColors(containerColor = Color(0xFFE0E0E0))
            ) {
                Text("인증 코드 발송", color = Color.Black)
            }

            // 인증 코드 입력
            OutlinedTextField(
                value = emailCode,
                onValueChange = { emailCode = it },
                label = { Text("인증 코드 입력") },
                modifier = Modifier
                    .fillMaxWidth()
                    .padding(vertical = 8.dp),
                keyboardOptions = KeyboardOptions(keyboardType = KeyboardType.Number),
                singleLine = true
            )

            // 인증 확인 버튼
            Button(
                onClick = {
                    // TODO: 서버에 email + emailCode 전송하여 인증 확인
                    isEmailVerified = true // ← 실제로는 성공 응답 후 변경
                    scope.launch {
                        viewModel.verifyCode(emailCode)
                        snackbarHostState.showSnackbar("이메일 인증이 완료되었습니다.")
                    }
                },
                modifier = Modifier
                    .align(Alignment.End)
                    .padding(bottom = 16.dp),
                colors = ButtonDefaults.buttonColors(containerColor = Color(0xFFD0BCFF)),
                enabled = email.isNotBlank() && emailCode.isNotBlank() && !isEmailVerified
            ) {
                Text("인증 확인", color = Color.Black)
            }

            Spacer(modifier = Modifier.height(24.dp))

            Button(
                onClick = {
                    when {
                        current_password.isBlank() ||
                        new_password.isBlank() ||
                        confirmPassword.isBlank() -> {
                            scope.launch {
                                snackbarHostState.showSnackbar("모든 필드를 입력해주세요.")
                            }
                        }
                        new_password != confirmPassword -> {
                            scope.launch {
                                snackbarHostState.showSnackbar("새 비밀번호가 일치하지 않습니다.")
                            }
                        }
                        else -> {
                            isLoading = true
                            // TODO: API 호출하여 비밀번호 변경 로직 수행
                            // ex) UserRepository.changePassword(currentPassword, newPassword)
                            viewModel.updatePwd(current_password, new_password)
                            // 결과에 따라
                            isLoading = false
                            onPasswordChanged()
                            scope.launch {
                                snackbarHostState.showSnackbar("비밀번호가 변경되었습니다.")

                            }
                        }
                    }
                },
                modifier = Modifier
                    .fillMaxWidth()
                    .height(56.dp),
                colors = ButtonDefaults.buttonColors(containerColor = Color(0xFFD0BCFF)),
                shape = RoundedCornerShape(8.dp)
            ) {
                if (isLoading) {
                    CircularProgressIndicator(modifier = Modifier.size(24.dp))
                } else {
                    Text(
                        text = "비밀번호 변경",
                        fontSize = 16.sp,
                        color = Color.Black,
                        fontWeight = FontWeight.Medium
                    )
                }
            }
        }
    }
}

fun isValidEmail(email: String): Boolean {
    return android.util.Patterns.EMAIL_ADDRESS.matcher(email).matches()
}
