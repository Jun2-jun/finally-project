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
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.lifecycle.viewmodel.compose.viewModel
import kotlinx.coroutines.launch
import com.android.hospitalAPP.viewmodel.WithdrawAccountViewModel   // ✅ ViewModel import 변경
import com.android.hospitalAPP.data.ApiResult


@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun WithdrawAccountScreen(
    onNavigateBack: () -> Unit,
    onWithdrawConfirm: () -> Unit,
    viewModel: WithdrawAccountViewModel = viewModel()
) {
    val snackbarHostState = remember { SnackbarHostState() }
    val scope = rememberCoroutineScope()

    var current_password by remember { mutableStateOf("") }
    var isLoading by remember { mutableStateOf(false) }

    val withdrawResult by viewModel.withdrawResult  // ✅ ViewModel의 상태 관찰

    // ✅ 탈퇴 결과에 따라 동작
    LaunchedEffect(withdrawResult) {
        when (withdrawResult) {
            is ApiResult.Success -> {
                onWithdrawConfirm()
            }
            is ApiResult.Error -> {
                val message = (withdrawResult as ApiResult.Error).message
                snackbarHostState.showSnackbar(message)
            }
            else -> {}
        }
    }

    Scaffold(
        topBar = {
            TopAppBar(
                title = { Text("회원탈퇴") },
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

            Spacer(modifier = Modifier.height(24.dp))

            Button(
                onClick = {
                    if (current_password.isBlank()) {
                        scope.launch {
                            snackbarHostState.showSnackbar("비밀번호를 입력해주세요.")
                        }
                    } else {
                        viewModel.withdrawAccount(current_password)  // ✅ 여기서 호출
                        isLoading = true
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
                        text = "회원탈퇴",
                        fontSize = 16.sp,
                        color = Color.Black,
                        fontWeight = FontWeight.Medium
                    )
                }
            }
        }
    }
}