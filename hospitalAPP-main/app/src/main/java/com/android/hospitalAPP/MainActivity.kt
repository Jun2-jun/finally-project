// MainActivity.kt - Entry point with navigation setup
package com.android.hospitalAPP

import android.os.Bundle
import android.util.Log
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.compose.foundation.background
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Color
import androidx.navigation.compose.rememberNavController
import com.android.hospitalAPP.data.UserRepository
import com.android.hospitalAPP.navigation.AppNavigation
import com.android.hospitalAPP.ui.theme.HospitalAppTheme
import com.kakao.sdk.common.util.Utility
import com.kakao.vectormap.KakaoMapSdk
import android.widget.Toast

// ✅ 앱의 Entry Point - MainActivity
class MainActivity : ComponentActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)

        if (RootCheck.isDeviceRootedNative()) {
            Toast.makeText(this, "루팅된 기기입니다. 앱을 종료합니다.", Toast.LENGTH_LONG).show()
            finish()
        }
        // ✅ 카카오 키 해시 출력 (로그인, 지도 연동용)
        var keyHash = Utility.getKeyHash(this)
        Log.d("KeyHash", "KeyHash: $keyHash")

        // ✅ 카카오 지도 SDK 초기화
        KakaoMapSdk.init(this,"bf105d2a0b3861e39aff0e8f49f7f0ce")
        // UserRepository에 컨텍스트 설정
        UserRepository.getInstance().setContext(applicationContext)

        // ✅ Compose 화면 설정
        setContent {
            // 테마 적용
            HospitalAppTheme {
                Box(
                    modifier = Modifier
                        .fillMaxSize()
                        .background(Color.White) // 기본 배경 흰색
                ) {
                    val navController = rememberNavController() // 네비게이션 컨트롤러 생성
                    AppNavigation(navController = navController) // 네비게이션 그래프 연결
                }
            }
        }

    }
}