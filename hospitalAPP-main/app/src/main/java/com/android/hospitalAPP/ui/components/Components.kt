// Components.kt - Reusable UI components
package com.android.hospitalAPP.ui.components

import androidx.compose.foundation.background
import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.*

import androidx.compose.material3.*
import androidx.compose.runtime.Composable
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.res.painterResource

import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import com.android.hospitalAPP.navigation.Screen
import com.android.hospitalAPP.ui.theme.*
import androidx.compose.ui.tooling.preview.Preview



@Composable
fun BottomNavigation(
    currentRoute: String,
    onNavigate: (String) -> Unit
) {
    val dimens = appDimens()

    Row(
        modifier = Modifier
            .fillMaxWidth()
            .background(Color.White)
            .padding(vertical = dimens.paddingMedium.dp),
        horizontalArrangement = Arrangement.SpaceAround
    ) {
        BottomNavigationItem(
            text = "홈",
            iconRes = android.R.drawable.ic_menu_compass,
            isSelected = currentRoute == Screen.Home.route,
            onClick = { onNavigate(Screen.Home.route) }
        )

        BottomNavigationItem(
            text = "닥터 퓨처(AI)",
            iconRes = android.R.drawable.ic_menu_myplaces,
            isSelected = currentRoute == Screen.MyDdocDoc.route,
            onClick = { onNavigate(Screen.MyDdocDoc.route) }
        )

        BottomNavigationItem(
            text = "커뮤니티",
            iconRes = android.R.drawable.ic_menu_share,
            isSelected = currentRoute == Screen.Community.route,
            onClick = { onNavigate(Screen.Community.route) }
        )

        BottomNavigationItem(
            text = "마이페이지",
            iconRes = android.R.drawable.ic_menu_my_calendar,
            isSelected = currentRoute == Screen.MyPage.route,
            onClick = { onNavigate(Screen.MyPage.route) }
        )
    }
}

@Preview
@Composable
fun BottomNavigationPreview() {
    BottomNavigation(currentRoute = Screen.Home.route, onNavigate = {})
}

@Composable
fun BottomNavigationItem(
    text: String,
    iconRes: Int,
    isSelected: Boolean,
    onClick: () -> Unit
) {
    val dimens = appDimens()

    Column(
        modifier = Modifier
            .clickable(onClick = onClick)
            .padding(dimens.paddingSmall.dp),
        horizontalAlignment = Alignment.CenterHorizontally
    ) {
        Icon(
            painter = painterResource(id = iconRes),
            contentDescription = text,
            tint = if (isSelected) Color.Black else TextSecondary,
            modifier = Modifier.size(dimens.iconSize.dp)
        )

        Text(
            text = text,
            fontSize = 12.sp,
            color = if (isSelected) Color.Black else TextSecondary
        )
    }
}

