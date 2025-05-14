package com.android.hospitalAPP.ui.screens

import androidx.compose.foundation.layout.*
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.verticalScroll
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.ArrowBack
import androidx.compose.material3.OutlinedTextField
import androidx.compose.material3.Text
import androidx.compose.material3.ExposedDropdownMenuBox
import androidx.compose.material3.ExposedDropdownMenuDefaults
import androidx.compose.material3.DropdownMenuItem
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Modifier
import androidx.compose.ui.unit.dp
import androidx.compose.ui.Alignment
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.ui.unit.sp
import com.android.hospitalAPP.data.UserRepository
import com.android.hospitalAPP.viewmodel.HealthInfoInputViewModel
import android.widget.Toast
import androidx.compose.ui.platform.LocalContext
import com.android.hospitalAPP.navigation.Screen

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun HealthInfoInputScreen(
    viewModel: HealthInfoInputViewModel,
    onNavigateBack: () -> Unit,
    navigateToScreen: (String) -> Unit,
    onNavigateHome: () -> Unit
) {
    val userRepository = UserRepository.getInstance()
    val currentUser by userRepository.currentUser.collectAsState()
    val dimens = 16.dp

    val context = LocalContext.current
    val state by viewModel.updateUiState.collectAsState()

    // 성공 시 토스트 + 홈 이동
    LaunchedEffect(state) {
        when (state) {
            is HealthInfoInputViewModel.UpdateState.Success -> {
                Toast.makeText(context, (state as HealthInfoInputViewModel.UpdateState.Success).message, Toast.LENGTH_SHORT).show()
                onNavigateHome()
            }
            is HealthInfoInputViewModel.UpdateState.Error -> {
                Toast.makeText(context, (state as HealthInfoInputViewModel.UpdateState.Error).message, Toast.LENGTH_SHORT).show()
            }
            else -> {}
        }
    }
    LaunchedEffect(currentUser) {
        if (currentUser == null) {
            navigateToScreen(Screen.Login.route)
        }
    }
    LaunchedEffect(Unit) {
        viewModel.loadHealthInfo()
    }

    Scaffold(
        topBar = {
            TopAppBar(
                title = { Text("환자 기본 정보") },
                navigationIcon = {
                    IconButton(onClick = onNavigateBack) {
                        Icon(Icons.Filled.ArrowBack, contentDescription = "뒤로가기")
                    }
                }
            )
        }
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
                    .padding(dimens)
                    .verticalScroll(rememberScrollState())
            ) {
                // 첫 번째 줄: 혈액형 + 알레르기
                Row(modifier = Modifier.fillMaxWidth()) {
                    Box(modifier = Modifier.weight(1f).padding(end = 8.dp)) {
                        BloodTypeDropdown(viewModel)
                    }
                    Box(modifier = Modifier.weight(1f).padding(start = 8.dp)) {
                        OutlinedTextField(
                            value = viewModel.allergyInfo.value,
                            onValueChange = { viewModel.allergyInfo.value = it },
                            label = { Text("알레르기 정보") },
                            modifier = Modifier.fillMaxWidth(),
                            shape = RoundedCornerShape(8.dp)
                        )
                    }
                }

                Spacer(modifier = Modifier.height(dimens))

                // 두 번째 줄: 키 + 몸무게
                Row(modifier = Modifier.fillMaxWidth()) {
                    Box(modifier = Modifier.weight(1f).padding(end = 8.dp)) {
                        Row(
                            modifier = Modifier.fillMaxWidth(),
                            verticalAlignment = Alignment.CenterVertically
                        ) {
                            OutlinedTextField(
                                value = viewModel.heightCm.value,
                                onValueChange = { viewModel.heightCm.value = it },
                                label = { Text("키") },
                                modifier = Modifier.weight(1f),
                                shape = RoundedCornerShape(8.dp)
                            )
                            Spacer(modifier = Modifier.width(4.dp))
                            Text("cm")
                        }
                    }

                    Box(modifier = Modifier.weight(1f).padding(start = 8.dp)) {
                        Row(
                            modifier = Modifier.fillMaxWidth(),
                            verticalAlignment = Alignment.CenterVertically
                        ) {
                            OutlinedTextField(
                                value = viewModel.weightKg.value,
                                onValueChange = { viewModel.weightKg.value = it },
                                label = { Text("몸무게") },
                                modifier = Modifier.weight(1f),
                                shape = RoundedCornerShape(8.dp)
                            )
                            Spacer(modifier = Modifier.width(4.dp))
                            Text("kg")
                        }
                    }
                }

                Spacer(modifier = Modifier.height(dimens))

                // 복용 중인 약물 (새로 추가됨)
                OutlinedTextField(
                    value = viewModel.currentMedications.value,
                    onValueChange = { viewModel.currentMedications.value = it },
                    label = { Text("복용 중인 약물") },
                    modifier = Modifier
                        .fillMaxWidth()
                        .height(100.dp),
                    maxLines = 4,
                    shape = RoundedCornerShape(8.dp)
                )

                Spacer(modifier = Modifier.height(dimens))

// 흡연 상태 라디오 그룹 (세 가지 옵션)
                Column(
                    modifier = Modifier
                        .fillMaxWidth()
                        .padding(vertical = 8.dp)
                ) {
                    Text("흡연 상태", fontSize = 16.sp)
                    Spacer(modifier = Modifier.height(4.dp))

                    Row(
                        modifier = Modifier.fillMaxWidth(),
                        verticalAlignment = Alignment.CenterVertically
                    ) {
                        RadioButton(
                            selected = viewModel.smokingStatus.value == "NON_SMOKER",
                            onClick = { viewModel.smokingStatus.value = "NON_SMOKER" }
                        )
                        Spacer(modifier = Modifier.width(4.dp))
                        Text("비흡연자")
                    }

                    Row(
                        modifier = Modifier.fillMaxWidth(),
                        verticalAlignment = Alignment.CenterVertically
                    ) {
                        RadioButton(
                            selected = viewModel.smokingStatus.value == "CURRENT_SMOKER",
                            onClick = { viewModel.smokingStatus.value = "CURRENT_SMOKER" }
                        )
                        Spacer(modifier = Modifier.width(4.dp))
                        Text("현재 흡연 중")
                    }

                    Row(
                        modifier = Modifier.fillMaxWidth(),
                        verticalAlignment = Alignment.CenterVertically
                    ) {
                        RadioButton(
                            selected = viewModel.smokingStatus.value == "FORMER_SMOKER",
                            onClick = { viewModel.smokingStatus.value = "FORMER_SMOKER" }
                        )
                        Spacer(modifier = Modifier.width(4.dp))
                        Text("과거 흡연자")
                    }
                }

                Spacer(modifier = Modifier.height(dimens))

                // 과거 질병 이력 (멀티라인, 높이 증가)
                OutlinedTextField(
                    value = viewModel.pastIllnesses.value,
                    onValueChange = { viewModel.pastIllnesses.value = it },
                    label = { Text("과거 질병 이력") },
                    modifier = Modifier
                        .fillMaxWidth()
                        .height(150.dp),
                    maxLines = 5,
                    shape = RoundedCornerShape(8.dp)
                )

                Spacer(modifier = Modifier.height(dimens))

                // 만성 질환 (멀티라인, 높이 증가)
                OutlinedTextField(
                    value = viewModel.chronicDiseases.value,
                    onValueChange = { viewModel.chronicDiseases.value = it },
                    label = { Text("만성 질환") },
                    modifier = Modifier
                        .fillMaxWidth()
                        .height(150.dp),
                    maxLines = 5,
                    shape = RoundedCornerShape(8.dp)
                )

                // 저장 버튼
                Button(
                    onClick = { viewModel.submitHealthInfo() },
                    modifier = Modifier
                        .fillMaxWidth()
                        .padding(16.dp)
                ) {
                    Text("저장하기")
                }
            }
        }
    }
}


/*
    혈액형 드롭다운 박스
 */
@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun BloodTypeDropdown(
    viewModel: HealthInfoInputViewModel
) {
    val bloodTypes = listOf("A+", "A-", "B+", "B-", "AB+", "AB-", "O+", "O-")
    var expanded by remember { mutableStateOf(false) }

    ExposedDropdownMenuBox(
        expanded = expanded,
        onExpandedChange = { expanded = !expanded }
    ) {
        OutlinedTextField(
            readOnly = true,
            value = viewModel.bloodType.value.ifEmpty { "선택하세요" }, // 기본 표시값
            onValueChange = { viewModel.bloodType.value = it },
            label = { Text("혈액형") },
            modifier = Modifier
                .fillMaxWidth()
                .menuAnchor(),
            trailingIcon = {
                ExposedDropdownMenuDefaults.TrailingIcon(expanded = expanded)
            },
            colors = ExposedDropdownMenuDefaults.outlinedTextFieldColors(
                focusedBorderColor = MaterialTheme.colorScheme.primary,
                unfocusedBorderColor = MaterialTheme.colorScheme.outline,
                focusedLabelColor = MaterialTheme.colorScheme.primary,
                unfocusedLabelColor = MaterialTheme.colorScheme.outline
            ),
            shape = RoundedCornerShape(8.dp),
            singleLine = true
        )

        ExposedDropdownMenu(
            expanded = expanded,
            onDismissRequest = { expanded = false }
        ) {
            bloodTypes.forEach { type ->
                DropdownMenuItem(
                    text = {
                        Text(
                            text = type,
                            color = if (viewModel.bloodType.value == type)
                                MaterialTheme.colorScheme.primary else MaterialTheme.colorScheme.onSurface
                        )
                    },
                    onClick = {
                        viewModel.bloodType.value = type
                        expanded = false
                    }
                )
            }
        }
    }
}