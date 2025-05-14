// ReservationHistoryScreen.kt
package com.android.hospitalAPP.ui.screens

import androidx.compose.foundation.background
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.ArrowBack
import androidx.compose.material.icons.filled.Email
import androidx.compose.material.icons.filled.LocationOn
import androidx.compose.material.icons.filled.Phone
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.graphics.vector.ImageVector
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.style.TextAlign
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import androidx.lifecycle.viewmodel.compose.viewModel
import com.android.hospitalAPP.data.UserRepository
import com.android.hospitalAPP.viewmodel.Reservation
import com.android.hospitalAPP.navigation.Screen
import com.android.hospitalAPP.viewmodel.ReservationHistoryViewModel

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun ReservationHistoryScreen(
    onNavigateBack: () -> Unit,
    navigateToScreen: (String) -> Unit = {},
    viewModel: ReservationHistoryViewModel = viewModel()
) {
    LaunchedEffect(key1 = Unit) {
        viewModel.loadReservations()
    }

    val uiState by viewModel.uiState.collectAsState()

    val userRepository = UserRepository.getInstance()
    val currentUser by userRepository.currentUser.collectAsState()
    LaunchedEffect(currentUser) {
        if (currentUser == null) {
            navigateToScreen(Screen.Login.route)
        }
    }
    Scaffold(
        topBar = {
            TopAppBar(
                title = { Text("예약 내역") },
                navigationIcon = {
                    IconButton(onClick = onNavigateBack) {
                        Icon(Icons.Filled.ArrowBack, contentDescription = "뒤로가기")
                    }
                },
                colors = TopAppBarDefaults.topAppBarColors(
                    containerColor = Color.White
                )
            )
        }
    ) { paddingValues ->
        when (uiState) {
            is ReservationHistoryViewModel.ReservationHistoryUiState.Loading -> {
                Box(
                    modifier = Modifier
                        .fillMaxSize()
                        .padding(paddingValues),
                    contentAlignment = Alignment.Center
                ) {
                    CircularProgressIndicator(color = Color(0xFFD0BCFF))
                }
            }
            is ReservationHistoryViewModel.ReservationHistoryUiState.NotLoggedIn -> {
                Box(
                    modifier = Modifier
                        .fillMaxSize()
                        .padding(paddingValues),
                    contentAlignment = Alignment.Center
                ) {
                    Column(horizontalAlignment = Alignment.CenterHorizontally) {
                        Text("로그인이 필요한 서비스입니다.", fontSize = 18.sp)
                        Spacer(modifier = Modifier.height(16.dp))
                        Button(
                            onClick = { navigateToScreen(Screen.Login.route) },
                            colors = ButtonDefaults.buttonColors(containerColor = Color(0xFFD0BCFF)),
                            shape = RoundedCornerShape(8.dp)
                        ) {
                            Text("로그인하기", color = Color.Black)
                        }
                    }
                }
            }
            is ReservationHistoryViewModel.ReservationHistoryUiState.Empty -> {
                Box(
                    modifier = Modifier
                        .fillMaxSize()
                        .padding(paddingValues)
                        .padding(16.dp),
                    contentAlignment = Alignment.Center
                ) {
                    Column(horizontalAlignment = Alignment.CenterHorizontally) {
                        Text(
                            "예약 내역이 없습니다.",
                            fontSize = 18.sp,
                            color = Color.Gray,
                            textAlign = TextAlign.Center
                        )
                        Spacer(modifier = Modifier.height(16.dp))
                        Button(
                            onClick = { /* 검색 기능 추가 */ },
                            colors = ButtonDefaults.buttonColors(containerColor = Color(0xFFD0BCFF)),
                            shape = RoundedCornerShape(8.dp)
                        ) {
                            Text("병원 검색하기", color = Color.Black)
                        }
                    }
                }
            }
            is ReservationHistoryViewModel.ReservationHistoryUiState.Success -> {
                val reservations = (uiState as ReservationHistoryViewModel.ReservationHistoryUiState.Success).reservations
                Column(
                    modifier = Modifier
                        .fillMaxSize()
                        .padding(paddingValues)
                        .padding(16.dp)
                ) {
                    Text(
                        "총 ${reservations.size}건의 예약이 있습니다.",
                        fontSize = 14.sp,
                        color = Color.Gray,
                        modifier = Modifier.padding(vertical = 8.dp)
                    )
                    LazyColumn(
                        modifier = Modifier.fillMaxSize(),
                        verticalArrangement = Arrangement.spacedBy(16.dp)
                    ) {
                        items(reservations) { reservation ->
                            ReservationCard(reservation = reservation)
                        }
                    }
                }
            }
            is ReservationHistoryViewModel.ReservationHistoryUiState.Error -> {
                val errorMessage = (uiState as ReservationHistoryViewModel.ReservationHistoryUiState.Error).message
                Box(
                    modifier = Modifier
                        .fillMaxSize()
                        .padding(paddingValues),
                    contentAlignment = Alignment.Center
                ) {
                    Column(
                        horizontalAlignment = Alignment.CenterHorizontally,
                        verticalArrangement = Arrangement.Center,
                        modifier = Modifier.padding(16.dp)
                    ) {
                        Text(
                            "오류가 발생했습니다",
                            fontSize = 18.sp,
                            fontWeight = FontWeight.Bold,
                            color = Color.Red
                        )
                        Spacer(modifier = Modifier.height(8.dp))
                        Text(
                            errorMessage,
                            fontSize = 14.sp,
                            color = Color.Gray,
                            textAlign = TextAlign.Center
                        )
                        Spacer(modifier = Modifier.height(16.dp))
                        Button(
                            onClick = { viewModel.loadReservations() },
                            colors = ButtonDefaults.buttonColors(containerColor = Color(0xFFD0BCFF)),
                            shape = RoundedCornerShape(8.dp)
                        ) {
                            Text("다시 시도하기", color = Color.Black)
                        }
                    }
                }
            }
        }
    }
}

@Composable
fun ReservationCard(reservation: Reservation) {
    Card(
        modifier = Modifier.fillMaxWidth(),
        elevation = CardDefaults.cardElevation(4.dp),
        colors = CardDefaults.cardColors(containerColor = Color.White),
        shape = RoundedCornerShape(12.dp)
    ) {
        Column(
            modifier = Modifier
                .fillMaxWidth()
                .padding(16.dp)
        ) {
            Row(
                modifier = Modifier.fillMaxWidth(),
                horizontalArrangement = Arrangement.SpaceBetween,
                verticalAlignment = Alignment.CenterVertically
            ) {
                Text(
                    text = reservation.hospital,
                    fontSize = 18.sp,
                    fontWeight = FontWeight.Bold,
                )
                Box(
                    modifier = Modifier
                        .background(
                            color = when (reservation.status) {
                                "예약 확정" -> Color(0xFFE1F5FE)
                                "방문 완료" -> Color(0xFFE8F5E9)
                                else -> Color(0xFFFCE4EC)
                            },
                            shape = RoundedCornerShape(4.dp)
                        )
                        .padding(horizontal = 8.dp, vertical = 4.dp)
                ) {
                    Text(
                        text = reservation.status,
                        fontSize = 12.sp,
                        color = when (reservation.status) {
                            "예약 확정" -> Color(0xFF0288D1)
                            "방문 완료" -> Color(0xFF388E3C)
                            else -> Color(0xFFD81B60)
                        }
                    )
                }
            }

            Spacer(modifier = Modifier.height(8.dp))

            ReservationInfoRow(Icons.Default.LocationOn, reservation.address)
            ReservationInfoRow(Icons.Default.Phone, reservation.phone)
            ReservationInfoRow(Icons.Default.Email, reservation.email)

            if (reservation.message.isNotEmpty()) {
                Spacer(modifier = Modifier.height(8.dp))
                Text(
                    text = "메시지: ${reservation.message}",
                    fontSize = 14.sp,
                    color = Color.DarkGray
                )
            }

            Spacer(modifier = Modifier.height(16.dp))

            Row(
                modifier = Modifier.fillMaxWidth(),
                horizontalArrangement = Arrangement.spacedBy(8.dp)
            ) {
                when (reservation.status) {
                    "예약 확정" -> {
                        OutlinedButton(
                            onClick = { /* 취소 기능 */ },
                            modifier = Modifier.weight(1f),
                            shape = RoundedCornerShape(8.dp),
                            colors = ButtonDefaults.outlinedButtonColors(contentColor = Color.Gray)
                        ) {
                            Text("예약 취소")
                        }
                        Button(
                            onClick = { /* 변경 기능 */ },
                            modifier = Modifier.weight(1f),
                            shape = RoundedCornerShape(8.dp),
                            colors = ButtonDefaults.buttonColors(containerColor = Color(0xFFD0BCFF))
                        ) {
                            Text("예약 변경", color = Color.Black)
                        }
                    }
                    "방문 완료" -> {
                        Button(
                            onClick = { /* 리뷰 작성 기능 */ },
                            modifier = Modifier.fillMaxWidth(),
                            shape = RoundedCornerShape(8.dp),
                            colors = ButtonDefaults.buttonColors(containerColor = Color(0xFFD0BCFF))
                        ) {
                            Text("리뷰 작성하기", color = Color.Black)
                        }
                    }
                }
            }
        }
    }
}

@Composable
fun ReservationInfoRow(icon: ImageVector, text: String) {
    Row(
        modifier = Modifier.fillMaxWidth(),
        verticalAlignment = Alignment.CenterVertically
    ) {
        Icon(
            imageVector = icon,
            contentDescription = null,
            tint = Color.Gray,
            modifier = Modifier.size(20.dp)
        )
        Spacer(modifier = Modifier.width(8.dp))
        Text(
            text = text,
            fontSize = 14.sp,
            color = Color.DarkGray
        )
    }
}