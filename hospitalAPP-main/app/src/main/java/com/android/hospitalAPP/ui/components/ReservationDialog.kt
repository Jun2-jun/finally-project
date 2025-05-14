// ReservationDialog.kt
package com.android.hospitalAPP.ui.components

import androidx.compose.foundation.background
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.foundation.text.KeyboardOptions
import androidx.compose.foundation.verticalScroll
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.input.KeyboardType
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import androidx.compose.ui.window.Dialog
import com.android.hospitalAPP.data.PlaceSearchResult
import com.android.hospitalAPP.ui.theme.Purple80
import com.android.hospitalAPP.viewmodel.ReservationViewModel
import java.time.LocalDateTime
import java.time.ZoneId
import java.time.format.DateTimeFormatter
import android.app.DatePickerDialog
import android.app.TimePickerDialog
import java.util.Calendar
import androidx.compose.ui.platform.LocalContext
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.DateRange


/**
 * 병원 예약 다이얼로그
 * @param place 선택된 병원 정보
 * @param onDismiss 다이얼로그 닫기 콜백
 * @param onReservationSuccess 예약 성공 콜백
 * @param viewModel ReservationViewModel 인스턴스
 */
@Composable
fun ReservationDialog(
    place: PlaceSearchResult,
    onDismiss: () -> Unit,
    onReservationSuccess: () -> Unit,
    viewModel: ReservationViewModel
) {
    var message by remember { mutableStateOf("") }
    var email by remember { mutableStateOf("") }
    var reservation_time by remember { mutableStateOf("") } // 예약 시간 상태 추가

    // 예약 상태 관찰
    val reservationState by viewModel.reservationState.collectAsState()

    // 상태에 따른 사이드 이펙트
    LaunchedEffect(reservationState) {
        when (reservationState) {
            is ReservationViewModel.ReservationState.Success -> {
                onReservationSuccess()
            }
            else -> { /* 다른 상태는 처리하지 않음 */ }
        }
    }

    Dialog(
        onDismissRequest = onDismiss
    ) {
        Card(
            modifier = Modifier
                .fillMaxWidth()
                .padding(16.dp),
            shape = RoundedCornerShape(16.dp),
            colors = CardDefaults.cardColors(
                containerColor = Color.White
            )
        ) {
            Column(
                modifier = Modifier
                    .fillMaxWidth()
                    .padding(16.dp)
                    .verticalScroll(rememberScrollState())
            ) {
                // 다이얼로그 제목
                Text(
                    text = "병원 예약하기",
                    fontSize = 20.sp,
                    fontWeight = FontWeight.Bold,
                    color = Color.Black
                )

                Spacer(modifier = Modifier.height(16.dp))

                // 병원 정보
                Box(
                    modifier = Modifier
                        .fillMaxWidth()
                        .clip(RoundedCornerShape(8.dp))
                        .background(Color(0xFFF5F5F5))
                        .padding(12.dp)
                ) {
                    Column {
                        // 병원 이름
                        Text(
                            text = place.name,
                            fontWeight = FontWeight.Bold,
                            fontSize = 16.sp
                        )

                        Spacer(modifier = Modifier.height(4.dp))

                        // 병원 주소
                        Text(
                            text = place.address,
                            fontSize = 14.sp,
                            color = Color.Gray
                        )

                        if (place.phone.isNotEmpty()) {
                            Spacer(modifier = Modifier.height(4.dp))

                            // 병원 전화번호
                            Text(
                                text = place.phone,
                                fontSize = 14.sp,
                                color = Color.Gray
                            )
                        }
                    }
                }

                Spacer(modifier = Modifier.height(16.dp))

                // 예약 시간 입력 필드
                DateTimePickerField(
                    onDateTimeSelected = { selected ->
                        reservation_time = selected
                    }
                )

                Spacer(modifier = Modifier.height(12.dp))

                // 예약 메시지 입력 필드
                OutlinedTextField(
                    value = message,
                    onValueChange = { message = it },
                    label = { Text("증상 또는 예약 메시지") },
                    modifier = Modifier
                        .fillMaxWidth()
                        .height(120.dp),
                    shape = RoundedCornerShape(8.dp),
                    colors = OutlinedTextFieldDefaults.colors(
                        focusedBorderColor = Purple80,
                        unfocusedBorderColor = Color.LightGray
                    )
                )

                Spacer(modifier = Modifier.height(12.dp))

                // 이메일 입력 필드 (선택사항)
                OutlinedTextField(
                    value = email,
                    onValueChange = { email = it },
                    label = { Text("이메일 (선택사항)") },
                    modifier = Modifier.fillMaxWidth(),
                    shape = RoundedCornerShape(8.dp),
                    keyboardOptions = KeyboardOptions(keyboardType = KeyboardType.Email),
                    colors = OutlinedTextFieldDefaults.colors(
                        focusedBorderColor = Purple80,
                        unfocusedBorderColor = Color.LightGray
                    )
                )

                Spacer(modifier = Modifier.height(16.dp))

                // 예약 상태에 따른 메시지 표시
                when (reservationState) {
                    is ReservationViewModel.ReservationState.Error -> {
                        Text(
                            text = (reservationState as ReservationViewModel.ReservationState.Error).message,
                            color = Color.Red,
                            fontSize = 14.sp,
                            modifier = Modifier.padding(8.dp)
                        )
                    }
                    else -> { /* 다른 상태는 메시지 표시하지 않음 */ }
                }

                // 버튼 영역
                Row(
                    modifier = Modifier
                        .fillMaxWidth()
                        .padding(top = 16.dp),
                    horizontalArrangement = Arrangement.spacedBy(8.dp)
                ) {
                    // 취소 버튼
                    OutlinedButton(
                        onClick = {
                            viewModel.resetState()  // 상태 초기화
                            onDismiss()
                        },
                        modifier = Modifier.weight(1f),
                        shape = RoundedCornerShape(8.dp),
                        colors = ButtonDefaults.outlinedButtonColors(
                            contentColor = Color.Gray
                        )
                    ) {
                        Text("취소")
                    }

                    // 예약하기 버튼
                    Button(
                        onClick = {
                            if (message.isNotBlank()) {
                                viewModel.makeReservation(
                                    hospital = place.name,
                                    address = place.address,
                                    message = message,
                                    email = if (email.isNotBlank()) email else null,
                                    reservation_time = if (reservation_time.isNotBlank()) reservation_time else null // 예약 시간 추가
                                )
                            }
                        },
                        modifier = Modifier.weight(1f),
                        enabled = message.isNotBlank() && reservationState != ReservationViewModel.ReservationState.Loading,
                        colors = ButtonDefaults.buttonColors(
                            containerColor = Purple80
                        ),
                        shape = RoundedCornerShape(8.dp)
                    ) {
                        if (reservationState == ReservationViewModel.ReservationState.Loading) {
                            CircularProgressIndicator(
                                modifier = Modifier.size(24.dp),
                                color = Color.White,
                                strokeWidth = 2.dp
                            )
                        } else {
                            Text(
                                text = "예약하기",
                                color = Color.Black
                            )
                        }
                    }
                }
            }
        }
    }
}

@Composable
fun DateTimePickerField(
    label: String = "예약 희망 시간",
    onDateTimeSelected: (String) -> Unit
) {
    val context = LocalContext.current
    val formatter = DateTimeFormatter.ofPattern("yyyy-MM-dd HH:mm")
    val calendar = remember { Calendar.getInstance() }
    var dateTimeText by remember { mutableStateOf(formatter.format(LocalDateTime.now())) }

    OutlinedTextField(
        value = dateTimeText,
        onValueChange = {},
        label = { Text(label) },
        readOnly = true,
        modifier = Modifier.fillMaxWidth(),
        shape = RoundedCornerShape(8.dp),
        placeholder = { Text("예: YYYY-MM-DD HH:MM") },
        colors = OutlinedTextFieldDefaults.colors(
            focusedBorderColor = Purple80,
            unfocusedBorderColor = Color.LightGray
        ),
        trailingIcon = {
            IconButton(onClick = {
                // 날짜 먼저 선택
                DatePickerDialog(
                    context,
                    { _, year, month, day ->
                        // 시간 선택 다이얼로그로 연결
                        TimePickerDialog(
                            context,
                            { _, hour, minute ->
                                calendar.set(year, month, day, hour, minute)
                                val selected = formatter.format(
                                    calendar.time.toInstant().atZone(ZoneId.systemDefault()).toLocalDateTime()
                                )
                                dateTimeText = selected
                                onDateTimeSelected(selected)
                            },
                            calendar.get(Calendar.HOUR_OF_DAY),
                            calendar.get(Calendar.MINUTE),
                            true
                        ).show()
                    },
                    calendar.get(Calendar.YEAR),
                    calendar.get(Calendar.MONTH),
                    calendar.get(Calendar.DAY_OF_MONTH)
                ).show()
            }) {
                Icon(Icons.Default.DateRange, contentDescription = "날짜 선택")
            }
        }
    )
}