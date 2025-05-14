// LoginPage.kt
package com.android.hospitalAPP.ui.screens

import androidx.compose.foundation.layout.*
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.foundation.text.KeyboardOptions
import androidx.compose.foundation.verticalScroll
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.input.KeyboardType
import androidx.compose.ui.text.input.PasswordVisualTransformation
import androidx.compose.ui.text.style.TextAlign
import androidx.compose.ui.tooling.preview.Preview
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import androidx.lifecycle.viewmodel.compose.viewModel
import com.android.hospitalAPP.ui.theme.HospitalAppTheme
import com.android.hospitalAPP.viewmodel.LoginViewModel

@Composable
fun LoginPage(
    onLoginSuccess: () -> Unit = {},
    onNavigateToRegister: () -> Unit = {},
    viewModel: LoginViewModel = viewModel()
) {
    // ViewModel에서 상태 가져오기
    val userId by viewModel.userId.collectAsState()
    val password by viewModel.password.collectAsState()
    val rememberMe by viewModel.rememberMe.collectAsState()

    // LoginState 감시
    val loginState by viewModel.loginState.collectAsState()

    // 스낵바 표시를 위한 상태
    val snackbarHostState = remember { SnackbarHostState() }

    // 로그인 상태에 따른 사이드 이펙트 처리
    LaunchedEffect(loginState) {
        when (loginState) {
            is LoginViewModel.LoginState.Success -> {
                // 성공 메시지 표시
                snackbarHostState.showSnackbar(
                    message = (loginState as LoginViewModel.LoginState.Success).message,
                    duration = SnackbarDuration.Short
                )
                // 로그인 성공 콜백 호출
                onLoginSuccess()
            }
            is LoginViewModel.LoginState.Error -> {
                // 에러 메시지 표시
                snackbarHostState.showSnackbar(
                    message = (loginState as LoginViewModel.LoginState.Error).message,
                    duration = SnackbarDuration.Short
                )
            }
            else -> { /* 다른 상태는 처리하지 않음 */ }
        }
    }

    Scaffold(
        snackbarHost = { SnackbarHost(snackbarHostState) }
    ) { paddingValues ->
        Column(
            modifier = Modifier
                .fillMaxSize()
                .padding(paddingValues)
                .padding(16.dp)
                .verticalScroll(rememberScrollState()),
            horizontalAlignment = Alignment.CenterHorizontally
        ) {
            // 상단 여백
            Spacer(modifier = Modifier.height(40.dp))

            // 로그인 타이틀
            Text(
                text = "로그인",
                fontSize = 24.sp,
                fontWeight = FontWeight.Bold,
                color = Color.Black
            )

            Spacer(modifier = Modifier.height(40.dp))

            // 아이디/이메일 입력 필드
            OutlinedTextField(
                value = userId,
                onValueChange = { viewModel.updateUserId(it) },
                label = { Text("아이디 또는 이메일") },
                modifier = Modifier
                    .fillMaxWidth()
                    .padding(horizontal = 16.dp),
                shape = RoundedCornerShape(8.dp),
                singleLine = true
            )

            Spacer(modifier = Modifier.height(16.dp))

            // 비밀번호 입력 필드
            OutlinedTextField(
                value = password,
                onValueChange = { viewModel.updatePassword(it) },
                label = { Text("비밀번호") },
                modifier = Modifier
                    .fillMaxWidth()
                    .padding(horizontal = 16.dp),
                shape = RoundedCornerShape(8.dp),
                singleLine = true,
                visualTransformation = PasswordVisualTransformation(),
                keyboardOptions = KeyboardOptions(keyboardType = KeyboardType.Password)
            )

            Spacer(modifier = Modifier.height(8.dp))

            // 자동 로그인 체크박스
            Row(
                modifier = Modifier
                    .fillMaxWidth()
                    .padding(horizontal = 16.dp),
                verticalAlignment = Alignment.CenterVertically
            ) {
                Checkbox(
                    checked = rememberMe,
                    onCheckedChange = { viewModel.updateRememberMe(it) },
                    colors = CheckboxDefaults.colors(
                        checkedColor = Color(0xFFD0BCFF)
                    )
                )

                Text(
                    text = "자동 로그인",
                    color = Color.Gray,
                    fontSize = 14.sp
                )

                Spacer(modifier = Modifier.weight(1f))

                TextButton(
                    onClick = { /* TODO: 비밀번호 찾기 기능 */ }
                ) {
                    Text(
                        text = "비밀번호 찾기",
                        color = Color.Gray,
                        fontSize = 14.sp
                    )
                }
            }

            Spacer(modifier = Modifier.height(24.dp))

            // 로그인 버튼
            Button(
                onClick = {
                    if (userId.isNotEmpty() && password.isNotEmpty()) {
                        // ViewModel의 login 함수 호출
                        viewModel.login(userId, password, rememberMe)
                    }
                },
                modifier = Modifier
                    .fillMaxWidth()
                    .height(56.dp)
                    .padding(horizontal = 16.dp),
                colors = ButtonDefaults.buttonColors(
                    containerColor = Color(0xFFD0BCFF)
                ),
                shape = RoundedCornerShape(8.dp),
                // 로딩 상태일 때 버튼 비활성화
                enabled = loginState != LoginViewModel.LoginState.Loading
            ) {
                if (loginState == LoginViewModel.LoginState.Loading) {
                    // 로딩 중일 때 CircularProgressIndicator 표시
                    CircularProgressIndicator(
                        modifier = Modifier.size(24.dp),
                        color = Color.White,
                        strokeWidth = 2.dp
                    )
                } else {
                    Text(
                        text = "로그인",
                        fontSize = 16.sp,
                        color = Color.Black
                    )
                }
            }

            Spacer(modifier = Modifier.height(16.dp))

            Spacer(modifier = Modifier.height(24.dp))

            // 회원가입 안내 텍스트
            Row(
                modifier = Modifier.fillMaxWidth(),
                horizontalArrangement = Arrangement.Center,
                verticalAlignment = Alignment.CenterVertically
            ) {
                Text(
                    text = "아직 회원이 아니신가요?",
                    fontSize = 14.sp,
                    color = Color.Gray
                )

                TextButton(
                    onClick = { onNavigateToRegister() }
                ) {
                    Text(
                        text = "회원가입",
                        fontSize = 14.sp,
                        color = Color(0xFFD0BCFF),
                        fontWeight = FontWeight.Bold
                    )
                }
            }

            Spacer(modifier = Modifier.height(40.dp))
        }
    }
}

@Composable
fun SocialLoginButton(
    text: String,
    modifier: Modifier = Modifier,
    buttonColor: Color,
    onClick: () -> Unit = {}
) {
    Button(
        onClick = onClick,
        modifier = modifier
            .height(48.dp),
        colors = ButtonDefaults.buttonColors(
            containerColor = buttonColor
        ),
        shape = RoundedCornerShape(8.dp)
    ) {
        Text(
            text = text,
            fontSize = 14.sp,
            textAlign = TextAlign.Center,
            color = Color.Black
        )
    }
}

@Preview(showBackground = true)
@Composable
fun LoginPagePreview() {
    HospitalAppTheme {
        LoginPage()
    }
}