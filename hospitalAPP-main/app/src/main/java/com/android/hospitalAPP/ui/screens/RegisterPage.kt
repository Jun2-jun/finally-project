// RegisterPage.kt
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
import androidx.compose.ui.text.input.KeyboardType
import androidx.compose.ui.text.input.PasswordVisualTransformation
import androidx.compose.ui.tooling.preview.Preview
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import androidx.lifecycle.viewmodel.compose.viewModel
import com.android.hospitalAPP.ui.theme.HospitalAppTheme
import com.android.hospitalAPP.viewmodel.RegisterViewModel

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun RegisterPage(
    onNavigateBack: () -> Unit = {},
    onRegisterSuccess: () -> Unit = {},
    viewModel: RegisterViewModel = viewModel()
) {
    var email by remember { mutableStateOf("") }
    var userId by remember { mutableStateOf("") }
    var password by remember { mutableStateOf("") }
    var confirmPassword by remember { mutableStateOf("") }
    var address_detail by remember { mutableStateOf("") }
    var birthdate by remember { mutableStateOf("") }
    var phone by remember { mutableStateOf("") }
    var address by remember { mutableStateOf("") }
    var agreeTerms by remember { mutableStateOf(false) }

    // RegisterState 감시
    val registerState by viewModel.registerState.collectAsState()

    // 스낵바 표시를 위한 상태
    val snackbarHostState = remember { SnackbarHostState() }

    // 등록 상태에 따른 사이드 이펙트 처리
    LaunchedEffect(registerState) {
        when (registerState) {
            is RegisterViewModel.RegisterState.Success -> {
                // 성공 메시지 표시
                snackbarHostState.showSnackbar(
                    message = (registerState as RegisterViewModel.RegisterState.Success).message,
                    duration = SnackbarDuration.Short
                )
                // 등록 성공 콜백 호출
                onRegisterSuccess()
            }
            is RegisterViewModel.RegisterState.Error -> {
                // 에러 메시지 표시
                snackbarHostState.showSnackbar(
                    message = (registerState as RegisterViewModel.RegisterState.Error).message,
                    duration = SnackbarDuration.Short
                )
            }
            else -> { /* 다른 상태는 처리하지 않음 */ }
        }
    }

    Scaffold(
        topBar = {
            TopAppBar(
                title = { Text("회원가입") },
                navigationIcon = {
                    IconButton(onClick = onNavigateBack) {
                        Icon(Icons.Filled.ArrowBack, contentDescription = "뒤로가기")
                    }
                }
            )
        },
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
            Spacer(modifier = Modifier.height(16.dp))

            // 이메일 입력 필드
            OutlinedTextField(
                value = email,
                onValueChange = { email = it },
                label = { Text("이메일") },
                modifier = Modifier
                    .fillMaxWidth()
                    .padding(horizontal = 16.dp),
                shape = RoundedCornerShape(8.dp),
                singleLine = true,
                keyboardOptions = KeyboardOptions(keyboardType = KeyboardType.Email)
            )

            Spacer(modifier = Modifier.height(16.dp))

            // 아이디 입력 필드
            OutlinedTextField(
                value = userId,
                onValueChange = { userId = it },
                label = { Text("아이디 (4글자이상)") },
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
                onValueChange = { password = it },
                label = { Text("비밀번호 (6자리이상)") },
                modifier = Modifier
                    .fillMaxWidth()
                    .padding(horizontal = 16.dp),
                shape = RoundedCornerShape(8.dp),
                singleLine = true,
                visualTransformation = PasswordVisualTransformation(),
                keyboardOptions = KeyboardOptions(keyboardType = KeyboardType.Password)
            )

            Spacer(modifier = Modifier.height(16.dp))

            // 비밀번호 확인 필드
            OutlinedTextField(
                value = confirmPassword,
                onValueChange = { confirmPassword = it },
                label = { Text("비밀번호 확인") },
                modifier = Modifier
                    .fillMaxWidth()
                    .padding(horizontal = 16.dp),
                shape = RoundedCornerShape(8.dp),
                singleLine = true,
                visualTransformation = PasswordVisualTransformation(),
                keyboardOptions = KeyboardOptions(keyboardType = KeyboardType.Password),
                isError = password != confirmPassword && confirmPassword.isNotEmpty()
            )

            if (password != confirmPassword && confirmPassword.isNotEmpty()) {
                Text(
                    text = "비밀번호가 일치하지 않습니다",
                    color = MaterialTheme.colorScheme.error,
                    style = MaterialTheme.typography.bodySmall,
                    modifier = Modifier
                        .fillMaxWidth()
                        .padding(horizontal = 16.dp)
                )
            }

            Spacer(modifier = Modifier.height(16.dp))



            // 전화번호 입력 필드
            OutlinedTextField(
                value = phone,
                onValueChange = { phone = it },
                label = { Text("전화번호") },
                modifier = Modifier
                    .fillMaxWidth()
                    .padding(horizontal = 16.dp),
                shape = RoundedCornerShape(8.dp),
                singleLine = true,
                keyboardOptions = KeyboardOptions(keyboardType = KeyboardType.Phone)
            )

            Spacer(modifier = Modifier.height(16.dp))

            // 생년월일 입력 필드
            OutlinedTextField(
                value = birthdate,
                onValueChange = { birthdate = it },
                label = { Text("생년월일 (YYYY-MM-DD)") },
                modifier = Modifier
                    .fillMaxWidth()
                    .padding(horizontal = 16.dp),
                shape = RoundedCornerShape(8.dp),
                singleLine = true,
                keyboardOptions = KeyboardOptions(keyboardType = KeyboardType.Number)
            )

            Spacer(modifier = Modifier.height(16.dp))

            // 주소 입력 필드
            OutlinedTextField(
                value = address,
                onValueChange = { address = it },
                label = { Text("주소") },
                modifier = Modifier
                    .fillMaxWidth()
                    .padding(horizontal = 16.dp),
                shape = RoundedCornerShape(8.dp),
                singleLine = true
            )

            Spacer(modifier = Modifier.height(16.dp))


            // 상세주소 입력 필드
            OutlinedTextField(
                value = address_detail,
                onValueChange = { address_detail = it },
                label = { Text("상세주소 (예: 101동 101호") },
                modifier = Modifier
                    .fillMaxWidth()
                    .padding(horizontal = 16.dp),
                shape = RoundedCornerShape(8.dp),
                singleLine = true
            )

            Spacer(modifier = Modifier.height(16.dp))

            // 이용약관 동의
            Row(
                modifier = Modifier
                    .fillMaxWidth()
                    .padding(horizontal = 16.dp),
                verticalAlignment = Alignment.CenterVertically
            ) {
                Checkbox(
                    checked = agreeTerms,
                    onCheckedChange = { agreeTerms = it },
                    colors = CheckboxDefaults.colors(
                        checkedColor = Color(0xFFD0BCFF)
                    )
                )

                Text(
                    text = "이용약관 및 개인정보 처리방침에 동의합니다",
                    color = Color.Gray,
                    fontSize = 14.sp
                )
            }

            Spacer(modifier = Modifier.height(24.dp))

// RegisterPage.kt 파일의 회원가입 버튼 onClick 수정 부분
            Button(
                onClick = {
                    // 입력 검증
                    if (isInputValid(email, userId, password, confirmPassword, address_detail, birthdate, phone, address, agreeTerms)) {
                        // 회원가입 처리 - API 호출
                        viewModel.register(email, userId, password, address_detail, birthdate, phone, address)
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
                enabled = registerState != RegisterViewModel.RegisterState.Loading &&
                        isInputValid(email, userId, password, confirmPassword, address_detail, birthdate, phone, address, agreeTerms)
            ) {
                if (registerState == RegisterViewModel.RegisterState.Loading) {
                    // 로딩 중일 때 CircularProgressIndicator 표시
                    CircularProgressIndicator(
                        modifier = Modifier.size(24.dp),
                        color = Color.White,
                        strokeWidth = 2.dp
                    )
                } else {
                    Text(
                        text = "회원가입",
                        fontSize = 16.sp,
                        color = Color.Black
                    )
                }
            }

            Spacer(modifier = Modifier.height(24.dp))
        }
    }
}

private fun isInputValid(
    email: String,
    userId: String,
    password: String,
    confirmPassword: String,
    address_detail: String,
    birthdate: String,
    phone: String,
    address: String,
    agreeTerms: Boolean
): Boolean {
    // 기본적인 입력 검증 로직
    val isEmailValid = email.isNotEmpty() && email.contains("@")
    val isUserIdValid = userId.isNotEmpty() && userId.length >= 4
    val isPasswordValid = password.isNotEmpty() && password.length >= 6
    val isPasswordMatch = password == confirmPassword
    val isNameValid = address_detail.isNotEmpty()
    val isBirthdateValid = birthdate.isEmpty() || isValidDateFormat(birthdate) // 생년월일은 선택적이지만 입력 시 형식 검증
    val isPhoneValid = phone.isNotEmpty() && phone.length >= 10
    val isAddressValid = address.isEmpty() || address.length >= 5 // 주소는 선택적이지만 입력 시 최소 길이 검증

    return isEmailValid && isUserIdValid && isPasswordValid && isPasswordMatch &&
            isNameValid && isBirthdateValid && isPhoneValid && isAddressValid && agreeTerms
}

// 생년월일 형식 (YYYY-MM-DD) 검증
private fun isValidDateFormat(date: String): Boolean {
    val regex = Regex("""^\d{4}-\d{2}-\d{2}$""")
    return regex.matches(date)
}

@Preview(showBackground = true)
@Composable
fun RegisterPagePreview() {
    HospitalAppTheme {
        RegisterPage()
    }
}