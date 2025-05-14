// Navigation.kt - Updated with hospital search and reservation
package com.android.hospitalAPP.navigation

import androidx.compose.runtime.Composable
import androidx.compose.ui.Modifier
import androidx.navigation.NavHostController
import androidx.navigation.NavType
import androidx.navigation.compose.NavHost
import androidx.navigation.compose.composable
import androidx.navigation.navArgument
import com.android.hospitalAPP.ui.screens.CommunityScreen
import com.android.hospitalAPP.ui.screens.HomeScreen
import com.android.hospitalAPP.ui.screens.DoctorFutureScreen
import com.android.hospitalAPP.ui.screens.MyPageScreen
import com.android.hospitalAPP.ui.screens.LoginPage
import com.android.hospitalAPP.ui.screens.RegisterPage
import com.android.hospitalAPP.ui.screens.WritePostScreen
import com.android.hospitalAPP.ui.screens.ProfileManagementScreen
import com.android.hospitalAPP.ui.screens.ReservationHistoryScreen
import com.android.hospitalAPP.ui.screens.ChatBotScreen
import com.android.hospitalAPP.ui.screens.HospitalSearchResultScreen
import com.android.hospitalAPP.ui.screens.HealthInfoInputScreen
import com.android.hospitalAPP.ui.screens.HealthyMagazineScreen

import com.android.hospitalAPP.ui.screens.NoticeDetailScreen
import com.android.hospitalAPP.ui.screens.PostDetailScreen
import androidx.lifecycle.viewmodel.compose.viewModel
import com.android.hospitalAPP.viewmodel.CommunityViewModel
import androidx.compose.runtime.collectAsState
import androidx.compose.runtime.getValue
import androidx.compose.material3.Text
import com.android.hospitalAPP.ui.screens.WithdrawAccountScreen
import com.android.hospitalAPP.ui.screens.ChangePasswordScreen
import com.android.hospitalAPP.ui.screens.NotificationScreen
import com.android.hospitalAPP.ui.screens.FaqScreen

sealed class Screen(val route: String) {
    object Home : Screen("home")
    object MyDdocDoc : Screen("mydocdoc")
    object Community : Screen("community")
    object MyPage : Screen("mypage")
    object Login : Screen("login")
    object Register : Screen("register")
    object WritePost : Screen("write_post")

    object HealthyMagazine : Screen("HealthyMagazine")
    object ProfileManagement : Screen("profile_management")
    object ReservationHistory : Screen("reservation_history")
    object ChatBot : Screen("chatbot")
    object HospitalSearchResult : Screen("hospital_search_result/{query}") {
        fun createRoute(query: String) = "hospital_search_result/$query"
    }
    object NoticeDetail : Screen("notice_detail/{noticeId}") {
        fun createRoute(noticeId: Int) = "notice_detail/$noticeId"
    }
    object PostDetail : Screen("post_detail/{postId}") {
        fun createRoute(postId: Int) = "post_detail/$postId"
    }
    object ChangePassword : Screen("change_password")
    object WithdrawAccount : Screen("withdraw_account")

    object HealthInfoInput : Screen("health_info_input")

    object Notification : Screen("notification")

    object Faq : Screen("faq")
}

@Composable
fun AppNavigation(
    navController: NavHostController,
    modifier: Modifier = Modifier
) {
    NavHost(
        navController = navController,
        startDestination = Screen.Home.route,
        modifier = modifier
    ) {
        // 기존 화면 유지
        composable(route = Screen.Home.route) {
            HomeScreen(
                navigateToScreen = { route ->
                    navController.navigate(route)
                }
            )
        }

        composable(Screen.MyDdocDoc.route) {
            DoctorFutureScreen(
                navigateToScreen = { route ->
                    navController.navigate(route)
                }
            )
        }

        composable(Screen.HealthyMagazine.route) {
            HealthyMagazineScreen(
                navigateToScreen = { route ->
                    navController.navigate(route)
                }
            )
        }

        composable(Screen.Community.route) {
            CommunityScreen(
                navigateToScreen = { route ->
                    navController.navigate(route)
                }
            )
        }

        composable(Screen.MyPage.route) {
            MyPageScreen(
                navigateToScreen = { route ->
                    navController.navigate(route)
                }
            )
        }

        composable(Screen.Login.route) {
            LoginPage(
                onLoginSuccess = {
                    navController.navigate(Screen.Home.route) {
                        popUpTo(Screen.Login.route) { inclusive = true }
                    }
                },
                onNavigateToRegister = {
                    navController.navigate(Screen.Register.route)
                }
            )
        }

        composable(Screen.Register.route) {
            RegisterPage(
                onNavigateBack = {
                    navController.popBackStack()
                },
                onRegisterSuccess = {
                    navController.navigate(Screen.Login.route) {
                        popUpTo(Screen.Register.route) { inclusive = true }
                    }
                }
            )
        }

        composable(Screen.WritePost.route) {
            WritePostScreen(
                onNavigateBack = {
                    navController.popBackStack()
                },
                onPostSuccess = {
                    // 글 작성 성공 시 커뮤니티 화면으로 돌아감
                    navController.navigate(Screen.Community.route) {
                        popUpTo(Screen.WritePost.route) { inclusive = true }
                    }
                }
            )
        }

        // 내 정보 관리 화면
        composable(Screen.ProfileManagement.route) {
            ProfileManagementScreen(
                onNavigateBack         = { navController.popBackStack() },
                onNavigateChangePassword = { navController.navigate(Screen.ChangePassword.route) },
                onNavigateHome         = { navController.navigate(Screen.Home.route) },
                navigateToScreen = { navController.navigate(Screen.Login.route) }
            )
        }
        // 비밀번호 변경 화면
        composable(Screen.ChangePassword.route) {
            ChangePasswordScreen(
                onNavigateBack = { navController.popBackStack() },
                onPasswordChanged = { navController.popBackStack() }
            )
        }

        // 예약 내역 화면
        composable(Screen.ReservationHistory.route) {
            ReservationHistoryScreen(
                onNavigateBack = {
                    navController.popBackStack()
                }
            )
        }

        // 챗봇 화면
        composable(Screen.ChatBot.route) {
            ChatBotScreen(
                onNavigateBack = {
                    navController.popBackStack()
                }
            )
        }

        // 병원 검색 결과 화면 추가 - navigateToScreen 파라미터 추가
        composable(
            route = "hospital_search_result/{query}",
            arguments = listOf(
                navArgument("query") {
                    type = NavType.StringType
                }
            )
        ) { backStackEntry ->
            val query = backStackEntry.arguments?.getString("query") ?: ""
            HospitalSearchResultScreen(
                onNavigateBack = {
                    navController.popBackStack()
                },
                searchQuery = query,
                navigateToScreen = { route ->
                    navController.navigate(route)
                }
            )
        }

        //공지사항 상세 페이지
        composable(
            route = "notice_detail/{noticeId}",
            arguments = listOf(navArgument("noticeId") { type = NavType.IntType })
        ) { backStackEntry ->
            val noticeId = backStackEntry.arguments?.getInt("noticeId") ?: 0
            val viewModel: CommunityViewModel = viewModel()

            val noticeList: List<CommunityViewModel.Notice> by viewModel.notices.collectAsState()
            val notice = noticeList.find { it.id == noticeId }

            if (notice != null) {
                NoticeDetailScreen(
                    notice = notice,
                    onNavigateBack = { navController.popBackStack() }
                )
            } else {
                Text("공지사항을 찾을 수 없습니다.")
            }
        }
        // 댓글/대댓글 기능
        composable(
            route = Screen.PostDetail.route,
            arguments = listOf(navArgument("postId") { type = NavType.IntType })
        ) { backStackEntry ->
            val id = backStackEntry.arguments?.getInt("postId") ?: 0
            PostDetailScreen(
                postId = id,
                onNavigateBack = { navController.popBackStack() }
            )
        }

        // 회원탈퇴 화면
        composable(Screen.WithdrawAccount.route) {
            WithdrawAccountScreen(
                onNavigateBack = {
                    navController.popBackStack()
                },
                onWithdrawConfirm = {
                    // TODO: 탈퇴 처리 후 이동할 화면 정의
                    // 예: navController.navigate(Screen.Login.route) 또는 Snackbar 등
                    navController.popBackStack()  // 일단 뒤로 가기만 넣음
                }
            )
        }


        composable(route = Screen.HealthInfoInput.route) {
            HealthInfoInputScreen(
                viewModel = viewModel(),
                onNavigateBack = { navController.popBackStack() },
                onNavigateHome = { navController.navigate(Screen.Home.route) },
                navigateToScreen = { navController.navigate(Screen.Login.route) }
            )
        }

        composable(route = Screen.Notification.route) {
            NotificationScreen(
                onNavigateBack = { navController.popBackStack() }
            )
        }

        composable(route = Screen.Faq.route) {
            FaqScreen(
                onNavigateBack = { navController.popBackStack() }
            )
        }

    }
}