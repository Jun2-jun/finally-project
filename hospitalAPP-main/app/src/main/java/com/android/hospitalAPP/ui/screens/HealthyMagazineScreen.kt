package com.android.hospitalAPP.ui.screens

import androidx.compose.foundation.background
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.ArrowBack
import androidx.compose.material3.*
import androidx.compose.runtime.Composable
import androidx.compose.runtime.remember
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.style.TextOverflow
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import androidx.lifecycle.viewmodel.compose.viewModel
import com.android.hospitalAPP.navigation.Screen
import com.android.hospitalAPP.viewmodel.HomeViewModel

// 매거진 아티클 데이터 클래스
data class MagazineArticle(
    val id: Int,
    val title: String,
    val summary: String,
    val category: String,
    val date: String
)

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun HealthyMagazineScreen(
    viewModel: HomeViewModel= viewModel(),
    navigateToScreen: (String) -> Unit
) {
    // 샘플 기사 데이터
    val articles = remember {
        listOf(
            MagazineArticle(
                id = 1,
                title = "규칙적인 운동이 수면 질에 미치는 영향",
                summary = "운동을 통해 더 나은 수면을 취하는 방법을 알아보세요.",
                category = "수면 & 운동",
                date = "2025.05.07"
            ),
            MagazineArticle(
                id = 2,
                title = "영양 균형 잡힌 식단의 중요성",
                summary = "건강한 식습관이 전반적인 건강에 미치는 영향과 시작하는 방법",
                category = "영양 & 식이",
                date = "2025.05.05"
            ),
            MagazineArticle(
                id = 3,
                title = "스트레스 관리를 위한 명상 가이드",
                summary = "일상에서 쉽게 실천할 수 있는 5분 명상 테크닉",
                category = "멘탈 헬스",
                date = "2025.05.03"
            ),
            MagazineArticle(
                id = 4,
                title = "심혈관 건강을 위한 생활 습관",
                summary = "심장 건강을 지키기 위한 일상 속 실천 방법",
                category = "심장 건강",
                date = "2025.05.01"
            ),
            MagazineArticle(
                id = 5,
                title = "면역력 강화를 위한 식품 가이드",
                summary = "면역 체계를 지원하는 슈퍼푸드와 영양소",
                category = "면역 & 영양",
                date = "2025.04.28"
            ),
            MagazineArticle(
                id = 6,
                title = "디지털 디톡스의 건강상 이점",
                summary = "스크린 타임을 줄이고 정신 건강을 향상시키는 방법",
                category = "디지털 웰빙",
                date = "2025.04.25"
            ),
            MagazineArticle(
                id = 7,
                title = "요가로 유연성과 근력 향상하기",
                summary = "초보자도 쉽게 따라할 수 있는 기초 요가 포즈",
                category = "요가 & 피트니스",
                date = "2025.04.22"
            ),
            MagazineArticle(
                id = 8,
                title = "올바른 수분 섭취의 중요성",
                summary = "적절한 수분 섭취가 신체에 미치는 놀라운 효과",
                category = "건강 기초",
                date = "2025.04.20"
            ),
            MagazineArticle(
                id = 9,
                title = "건강한 관절을 위한 운동법",
                summary = "관절 건강을 유지하고 통증을 예방하는 운동 가이드",
                category = "관절 & 뼈 건강",
                date = "2025.04.18"
            ),
            MagazineArticle(
                id = 10,
                title = "계절별 알레르기 대처법",
                summary = "봄, 여름, 가을, 겨울 알레르기 증상 완화를 위한 팁",
                category = "알레르기 관리",
                date = "2025.04.15"
            )
        )
    }

    Scaffold(
        topBar = {
            TopAppBar(
                title = {
                    Text(
                        "건강 매거진",
                        fontWeight = FontWeight.Bold
                    )
                },
                navigationIcon = {
                    IconButton(onClick = {navigateToScreen(Screen.Home.route)}) {
                        Icon(
                            imageVector = Icons.Default.ArrowBack,
                            contentDescription = "뒤로가기"
                        )
                    }
                },
                colors = TopAppBarDefaults.topAppBarColors(
                    containerColor = Color(0xFF4CAF50),
                    titleContentColor = Color.White,
                    navigationIconContentColor = Color.White
                )
            )
        }
    ) { paddingValues ->
        LazyColumn(
            modifier = Modifier
                .fillMaxSize()
                .padding(paddingValues)
                .padding(horizontal = 16.dp),
            verticalArrangement = Arrangement.spacedBy(12.dp)
        ) {
            item {
                Spacer(modifier = Modifier.height(8.dp))

                // 최상단 배너
                FeaturedArticleBanner()

                Spacer(modifier = Modifier.height(16.dp))

                // 카테고리 섹션 타이틀
                Text(
                    text = "최신 건강 정보",
                    fontSize = 20.sp,
                    fontWeight = FontWeight.Bold,
                    modifier = Modifier.padding(vertical = 8.dp)
                )
            }

            // 기사 목록
            items(articles) { article ->
                ArticleItem(article = article)
            }

            item {
                Spacer(modifier = Modifier.height(16.dp))
            }
        }
    }
}

@Composable
fun FeaturedArticleBanner() {
    Card(
        modifier = Modifier
            .fillMaxWidth()
            .height(180.dp),
        shape = RoundedCornerShape(12.dp),
        elevation = CardDefaults.cardElevation(4.dp)
    ) {
        Box(modifier = Modifier.fillMaxSize()) {


            // 이미지 위에 어두운 오버레이 추가
            Box(
                modifier = Modifier
                    .fillMaxSize()
                    .background(Color.Black.copy(alpha = 0.5f))
            )

            // 텍스트 컨텐츠
            Column(
                modifier = Modifier
                    .fillMaxSize()
                    .padding(16.dp),
                verticalArrangement = Arrangement.Bottom
            ) {
                Text(
                    text = "이번 주 추천",
                    fontSize = 14.sp,
                    color = Color(0xFF4CAF50),
                    fontWeight = FontWeight.Bold,
                    modifier = Modifier
                        .background(
                            color = Color.White,
                            shape = RoundedCornerShape(4.dp)
                        )
                        .padding(horizontal = 8.dp, vertical = 4.dp)
                )

                Spacer(modifier = Modifier.height(8.dp))

                Text(
                    text = "건강한 노화를 위한 생활 습관 10가지",
                    fontSize = 22.sp,
                    fontWeight = FontWeight.Bold,
                    color = Color.White
                )

                Spacer(modifier = Modifier.height(4.dp))

                Text(
                    text = "나이가 들어도 건강하게 지내기 위한 전문가들의 조언",
                    fontSize = 14.sp,
                    color = Color.White.copy(alpha = 0.9f)
                )
            }
        }
    }
}

@Composable
fun ArticleItem(article: MagazineArticle) {
    Card(
        modifier = Modifier
            .fillMaxWidth(),
        shape = RoundedCornerShape(8.dp),
        elevation = CardDefaults.cardElevation(2.dp),
        colors = CardDefaults.cardColors(containerColor = MaterialTheme.colorScheme.surface)
    ) {
        Row(
            modifier = Modifier
                .fillMaxWidth()
                .padding(12.dp),
            horizontalArrangement = Arrangement.spacedBy(12.dp)
        ) {
            // 왼쪽 텍스트 컨텐츠
            Column(
                modifier = Modifier
                    .weight(1f)
                    .height(IntrinsicSize.Min)
            ) {
                // 카테고리
                Text(
                    text = article.category,
                    fontSize = 12.sp,
                    color = Color(0xFF4CAF50),
                    fontWeight = FontWeight.Bold
                )

                Spacer(modifier = Modifier.height(4.dp))

                // 제목
                Text(
                    text = article.title,
                    fontSize = 16.sp,
                    fontWeight = FontWeight.Bold,
                    maxLines = 2,
                    overflow = TextOverflow.Ellipsis
                )

                Spacer(modifier = Modifier.height(4.dp))

                // 요약
                Text(
                    text = article.summary,
                    fontSize = 14.sp,
                    color = Color.Gray,
                    maxLines = 2,
                    overflow = TextOverflow.Ellipsis
                )

                Spacer(modifier = Modifier.height(8.dp))

                // 날짜
                Text(
                    text = article.date,
                    fontSize = 12.sp,
                    color = Color.Gray
                )
            }
        }
    }
}

