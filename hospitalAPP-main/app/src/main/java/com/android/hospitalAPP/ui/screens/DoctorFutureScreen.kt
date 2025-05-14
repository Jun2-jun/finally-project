// DoctorFutureScreen.kt - 업데이트된 버전
package com.android.hospitalAPP.ui.screens

import androidx.compose.foundation.background
import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.shape.CircleShape
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.foundation.verticalScroll
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.KeyboardArrowRight
import androidx.compose.material3.*
import androidx.compose.runtime.Composable
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.style.TextAlign
import androidx.compose.ui.tooling.preview.Preview
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import androidx.lifecycle.viewmodel.compose.viewModel
import com.android.hospitalAPP.navigation.Screen
import com.android.hospitalAPP.ui.components.BottomNavigation
import com.android.hospitalAPP.ui.theme.Purple80
import com.android.hospitalAPP.viewmodel.HomeViewModel

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun DoctorFutureScreen(
    navigateToScreen: (String) -> Unit,
    viewModel: HomeViewModel = viewModel()
) {
    Scaffold(
        topBar = {
            TopAppBar(
                title = { Text("닥터 퓨처(AI)", fontWeight = FontWeight.Bold) },
                colors = TopAppBarDefaults.topAppBarColors(
                    containerColor = Color.White
                )
            )
        },
        bottomBar = {
            BottomNavigation(
                currentRoute = Screen.MyDdocDoc.route,
                onNavigate = navigateToScreen
            )
        }
    ) { paddingValues ->
        Column(
            modifier = Modifier
                .fillMaxSize()
                .padding(paddingValues)
                .verticalScroll(rememberScrollState())
        ) {
            // 헤더 영역
            Box(
                modifier = Modifier
                    .fillMaxWidth()
                    .background(Color(0xFFF5F5F5))
                    .padding(16.dp)
            ) {
                Text(
                    text = "건강 관리 서비스",
                    fontSize = 20.sp,
                    fontWeight = FontWeight.Bold
                )
            }

            // AI 챗봇 카드
            AIChatBotCard(
                onClick = { navigateToScreen(Screen.ChatBot.route) }
            )

            // 다른 서비스 카드들
            ServiceCard(
                title = "건강 체크리스트(미구현)",
                description = "매일 건강 상태를 체크하고 관리해보세요",
                onClick = { /* 건강 체크리스트 화면으로 이동 */ }
            )

            ServiceCard(
                title = "병원 예약 관리",
                description = "병원 예약 내역 확인 및 관리",
                onClick = { navigateToScreen(Screen.ReservationHistory.route) }
            )

            ServiceCard(
                title = "건강 다이어리(미구현)",
                description = "증상, 약 복용 기록 등을 관리하세요",
                onClick = { /* 건강 다이어리 화면으로 이동 */ }
            )

            ServiceCard(
                title = "가족 건강 관리(미구현)",
                description = "가족 구성원의 건강 정보를 한눈에",
                onClick = { /* 가족 건강 관리 화면으로 이동 */ }
            )

            // 미구현 태그 추가
            Box(
                modifier = Modifier
                    .fillMaxWidth()
                    .padding(16.dp),
                contentAlignment = Alignment.Center
            ) {
                Text(
                    text = "건강 체크리스트, 건강 다이어리, 가족 건강 관리는 현재 개발 중입니다",
                    fontSize = 12.sp,
                    color = Color.Gray,
                    textAlign = TextAlign.Center
                )
            }
        }
    }
}

@Composable
fun AIChatBotCard(onClick: () -> Unit) {
    Card(
        modifier = Modifier
            .fillMaxWidth()
            .padding(16.dp)
            .clickable(onClick = onClick),
        shape = RoundedCornerShape(16.dp),
        colors = CardDefaults.cardColors(
            containerColor = Purple80
        ),
        elevation = CardDefaults.cardElevation(4.dp)
    ) {
        Row(
            modifier = Modifier
                .fillMaxWidth()
                .padding(16.dp),
            verticalAlignment = Alignment.CenterVertically
        ) {
            // AI 아이콘
            Box(
                modifier = Modifier
                    .size(56.dp)
                    .clip(CircleShape)
                    .background(Color.White),
                contentAlignment = Alignment.Center
            ) {
                Text(
                    text = "AI",
                    fontSize = 24.sp,
                    fontWeight = FontWeight.Bold,
                    color = Color(0xFF6650a4)
                )
            }

            // 텍스트 영역
            Column(
                modifier = Modifier
                    .weight(1f)
                    .padding(horizontal = 16.dp)
            ) {
                Text(
                    text = "건강 상담 AI",
                    fontSize = 18.sp,
                    fontWeight = FontWeight.Bold,
                    color = Color.Black
                )

                Spacer(modifier = Modifier.height(4.dp))

                Text(
                    text = "건강 관련 질문을 AI에게 물어보세요",
                    fontSize = 14.sp,
                    color = Color.DarkGray
                )
            }

            // 화살표 아이콘
            Icon(
                imageVector = Icons.Default.KeyboardArrowRight,
                contentDescription = "바로가기",
                tint = Color.DarkGray
            )
        }
    }
}

@Composable
fun ServiceCard(
    title: String,
    description: String,
    onClick: () -> Unit
) {
    Card(
        modifier = Modifier
            .fillMaxWidth()
            .padding(horizontal = 16.dp, vertical = 8.dp)
            .clickable(onClick = onClick),
        shape = RoundedCornerShape(12.dp),
        colors = CardDefaults.cardColors(
            containerColor = Color.White
        ),
        elevation = CardDefaults.cardElevation(2.dp)
    ) {
        Row(
            modifier = Modifier
                .fillMaxWidth()
                .padding(16.dp),
            verticalAlignment = Alignment.CenterVertically
        ) {
            // 텍스트 영역
            Column(
                modifier = Modifier
                    .weight(1f)
                    .padding(end = 8.dp)
            ) {
                Text(
                    text = title,
                    fontSize = 16.sp,
                    fontWeight = FontWeight.Medium,
                    color = Color.Black
                )

                Spacer(modifier = Modifier.height(4.dp))

                Text(
                    text = description,
                    fontSize = 14.sp,
                    color = Color.Gray
                )
            }

            // 화살표 아이콘
            Icon(
                imageVector = Icons.Default.KeyboardArrowRight,
                contentDescription = "바로가기",
                tint = Color.Gray
            )
        }
    }
}

@Preview
@Composable
fun MyDdocDocScreenPreview() {
    DoctorFutureScreen(
        navigateToScreen = {}
    )
}