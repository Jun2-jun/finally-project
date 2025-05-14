// HospitalSearchResultScreen.kt - 예약 기능 추가 버전
package com.android.hospitalAPP.ui.screens

import androidx.compose.foundation.background
import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.*
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.style.TextOverflow
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import androidx.lifecycle.viewmodel.compose.viewModel
import com.android.hospitalAPP.data.PlaceSearchResult
import com.android.hospitalAPP.data.UserRepository
import com.android.hospitalAPP.navigation.Screen
import com.android.hospitalAPP.ui.components.KakaoMapView
import com.android.hospitalAPP.ui.components.ReservationDialog
import com.android.hospitalAPP.ui.theme.Purple80
import com.android.hospitalAPP.viewmodel.HospitalSearchViewModel
import com.android.hospitalAPP.viewmodel.ReservationViewModel

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun HospitalSearchResultScreen(
    onNavigateBack: () -> Unit,
    searchQuery: String,
    navigateToScreen: (String) -> Unit = {},
    hospitalSearchViewModel: HospitalSearchViewModel = viewModel(),
    reservationViewModel: ReservationViewModel = viewModel()
) {
    // 검색 결과 및 상태 관찰
    val searchResults by hospitalSearchViewModel.searchResults.collectAsState()
    val selectedPlace by hospitalSearchViewModel.selectedPlace.collectAsState()
    val isLoading by hospitalSearchViewModel.isLoading.collectAsState()
    val errorMessage by hospitalSearchViewModel.errorMessage.collectAsState()
    val lastQuery by hospitalSearchViewModel.lastQuery.collectAsState()

    // 예약 상태 관찰
    val reservationState by reservationViewModel.reservationState.collectAsState()

    // 예약 다이얼로그 표시 상태
    var showReservationDialog by remember { mutableStateOf(false) }

    // 로그인 상태 확인
    val userRepository = UserRepository.getInstance()
    val currentUser by userRepository.currentUser.collectAsState()

    // 스낵바 상태
    val snackbarHostState = remember { SnackbarHostState() }

    // 서울시청 좌표 (x: 경도, y: 위도) 현위치 값으로 변경 필요
    val seoulCityHallLongitude = 126.977963 // 경도(x)
    val seoulCityHallLatitude = 37.566535   // 위도(y)

    // 검색 수행
    LaunchedEffect(searchQuery) {
        if (searchQuery != lastQuery) {
            hospitalSearchViewModel.searchHospitals(searchQuery, seoulCityHallLongitude, seoulCityHallLatitude)
        }
    }

    // 예약 상태 변경 사이드 이펙트
    LaunchedEffect(reservationState) {
        when (reservationState) {
            is ReservationViewModel.ReservationState.Success -> {
                showReservationDialog = false
                snackbarHostState.showSnackbar(
                    message = (reservationState as ReservationViewModel.ReservationState.Success).message
                )
                reservationViewModel.resetState()
            }
            is ReservationViewModel.ReservationState.Error -> {
                if ((reservationState as ReservationViewModel.ReservationState.Error).message.contains("로그인")) {
                    showReservationDialog = false
                    snackbarHostState.showSnackbar(
                        message = "로그인이 필요한 서비스입니다.",
                        actionLabel = "로그인"
                    ).let { result ->
                        if (result == SnackbarResult.ActionPerformed) {
                            navigateToScreen(Screen.Login.route)
                        }
                    }
                    reservationViewModel.resetState()
                }
            }
            else -> { /* 다른 상태는 처리하지 않음 */ }
        }
    }

    Scaffold(
        topBar = {
            TopAppBar(
                title = { Text("'$searchQuery' 검색 결과") },
                navigationIcon = {
                    IconButton(onClick = onNavigateBack) {
                        Icon(Icons.Filled.ArrowBack, contentDescription = "뒤로가기")
                    }
                },
                colors = TopAppBarDefaults.topAppBarColors(
                    containerColor = Color.White
                )
            )
        },
        snackbarHost = { SnackbarHost(snackbarHostState) }
    ) { paddingValues ->
        Box(
            modifier = Modifier
                .fillMaxSize()
                .padding(paddingValues)
        ) {
            Column(
                modifier = Modifier.fillMaxSize()
            ) {
                // 지도 영역
                Box(
                    modifier = Modifier
                        .fillMaxWidth()
                        .weight(1f)
                ) {
                    KakaoMapView(
                        places = searchResults,
                        selectedPlace = selectedPlace,
                        onMarkerClick = { place ->
                            hospitalSearchViewModel.selectPlace(place)
                        }
                    )

                    // 로딩 인디케이터
                    if (isLoading) {
                        CircularProgressIndicator(
                            modifier = Modifier
                                .align(Alignment.Center)
                                .size(48.dp),
                            color = Purple80
                        )
                    }

                    // 검색 결과 카운트 표시
                    Card(
                        modifier = Modifier
                            .align(Alignment.TopStart)
                            .padding(16.dp),
                        colors = CardDefaults.cardColors(
                            containerColor = Color.White
                        ),
                        elevation = CardDefaults.cardElevation(4.dp)
                    ) {
                        Text(
                            text = if (isLoading) "검색 중..." else "검색 결과 ${searchResults.size}개",
                            modifier = Modifier.padding(horizontal = 12.dp, vertical = 8.dp),
                            fontSize = 14.sp,
                            fontWeight = FontWeight.Medium
                        )
                    }

                    // 에러 메시지
                    errorMessage?.let { message ->
                        Snackbar(
                            modifier = Modifier
                                .align(Alignment.BottomCenter)
                                .padding(16.dp),
                            action = {
                                TextButton(onClick = { hospitalSearchViewModel.clearError() }) {
                                    Text("확인")
                                }
                            }
                        ) {
                            Text(message)
                        }
                    }
                }

                // 병원 목록
                LazyColumn(
                    modifier = Modifier
                        .fillMaxWidth()
                        .height(200.dp)
                        .background(Color.White)
                ) {
                    if (searchResults.isEmpty() && !isLoading) {
                        item {
                            Box(
                                modifier = Modifier
                                    .fillMaxWidth()
                                    .height(200.dp),
                                contentAlignment = Alignment.Center
                            ) {
                                if (errorMessage == null) {
                                    Text(
                                        text = "검색 결과가 없습니다.",
                                        fontSize = 16.sp,
                                        color = Color.Gray
                                    )
                                }
                            }
                        }
                    } else {
                        items(searchResults) { place ->
                            HospitalItem(
                                place = place,
                                isSelected = selectedPlace?.id == place.id,
                                onClick = { hospitalSearchViewModel.selectPlace(place) },
                                onReservationClick = {
                                    if (currentUser != null) {
                                        // 로그인된 상태면 예약 다이얼로그 표시
                                        showReservationDialog = true
                                    } else {
                                        // 로그인이 필요하다는 메시지 표시
                                        reservationViewModel.makeReservation("", "", "") // 로그인 체크만 위한 호출
                                    }
                                }
                            )
                        }
                    }
                }
            }

            // 예약 다이얼로그
            if (showReservationDialog && selectedPlace != null) {
                ReservationDialog(
                    place = selectedPlace!!,
                    onDismiss = { showReservationDialog = false },
                    onReservationSuccess = {
                        // 예약 성공 처리 (이미 LaunchedEffect에서 처리됨)
                    },
                    viewModel = reservationViewModel
                )
            }
        }
    }
}

@Composable
fun HospitalItem(
    place: PlaceSearchResult,
    isSelected: Boolean,
    onClick: () -> Unit,
    onReservationClick: () -> Unit
) {
    Card(
        modifier = Modifier
            .fillMaxWidth()
            .padding(horizontal = 16.dp, vertical = 8.dp)
            .clickable(onClick = onClick),
        colors = CardDefaults.cardColors(
            containerColor = if (isSelected) Color(0xFFF0F0F0) else Color.White
        ),
        elevation = CardDefaults.cardElevation(if (isSelected) 4.dp else 2.dp)
    ) {
        Column(
            modifier = Modifier
                .fillMaxWidth()
                .padding(16.dp)
        ) {
            // 병원명 및 거리
            Row(
                modifier = Modifier.fillMaxWidth(),
                horizontalArrangement = Arrangement.SpaceBetween,
                verticalAlignment = Alignment.CenterVertically
            ) {
                Text(
                    text = place.name,
                    fontSize = 16.sp,
                    fontWeight = FontWeight.Bold,
                    maxLines = 1,
                    overflow = TextOverflow.Ellipsis,
                    modifier = Modifier.weight(1f)
                )

                // 거리 표시
                Text(
                    text = place.distance,
                    fontSize = 14.sp,
                    color = Color.Gray
                )
            }

            Spacer(modifier = Modifier.height(8.dp))

            // 주소
            Row(
                verticalAlignment = Alignment.CenterVertically
            ) {
                Icon(
                    imageVector = Icons.Default.LocationOn,
                    contentDescription = "주소",
                    tint = Color.Gray,
                    modifier = Modifier.size(16.dp)
                )

                Spacer(modifier = Modifier.width(4.dp))

                Text(
                    text = place.address,
                    fontSize = 14.sp,
                    color = Color.Gray,
                    maxLines = 1,
                    overflow = TextOverflow.Ellipsis,
                    modifier = Modifier.weight(1f)
                )
            }

            Spacer(modifier = Modifier.height(4.dp))

            // 전화번호 (있는 경우에만 표시)
            if (place.phone.isNotEmpty()) {
                Row(
                    verticalAlignment = Alignment.CenterVertically
                ) {
                    Icon(
                        imageVector = Icons.Default.Phone,
                        contentDescription = "전화번호",
                        tint = Color.Gray,
                        modifier = Modifier.size(16.dp)
                    )

                    Spacer(modifier = Modifier.width(4.dp))

                    Text(
                        text = place.phone,
                        fontSize = 14.sp,
                        color = Color.Gray
                    )
                }

                Spacer(modifier = Modifier.height(8.dp))
            }

            // 예약 버튼
            if (isSelected) {
                Button(
                    onClick = onReservationClick,
                    modifier = Modifier
                        .fillMaxWidth()
                        .height(40.dp),
                    colors = ButtonDefaults.buttonColors(
                        containerColor = Purple80
                    ),
                    shape = RoundedCornerShape(8.dp)
                ) {
                    Text(
                        text = "예약하기",
                        color = Color.Black
                    )
                }
            }
        }
    }
}