// Theme.kt - Define app theme and colors
package com.android.hospitalAPP.ui.theme

import androidx.compose.foundation.isSystemInDarkTheme
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.darkColorScheme
import androidx.compose.material3.lightColorScheme
import androidx.compose.runtime.Composable
import androidx.compose.runtime.CompositionLocalProvider
import androidx.compose.runtime.staticCompositionLocalOf
import androidx.compose.ui.graphics.Color


// Additional colors
val SearchBarBackground = Color(0xFFF0F0F0)
val TextSecondary = Color(0xFF888888)
val BannerBackground = Color(0xFFE6F5FA)
val BadgeBackground = Color(0xFFD1EBF5)
val PopularHospital = Color(0xFFFF7B4C)
val OpenHospital = Color(0xFF6495ED)

// Department colors
val PediatricsDept = Color(0xFFFFE082)
val EntDept = Color(0xFFD1E9FF)
val FamilyMedicineDept = Color(0xFFFFE0B2)
val ObGynDept = Color(0xFFF8BBD0)

// Theme dimensions
val LocalAppDimens = staticCompositionLocalOf { AppDimens() }

class AppDimens {
    val paddingSmall = 4
    val paddingMedium = 8
    val paddingLarge = 16
    val cornerRadius = 16
    val buttonCornerRadius = 12
    val iconSize = 24
    val bannerHeight = 150
    val buttonHeight = 60
    val growthBannerHeight = 100
    val departmentItemWidth = 80
    val departmentIconSize = 50
}

@Composable
fun HospitalAppTheme(
    darkTheme: Boolean = isSystemInDarkTheme(),
    content: @Composable () -> Unit
) {
    val colorScheme = if (darkTheme) {
        darkColorScheme(
            primary = Purple80,
            secondary = PurpleGrey80,
            tertiary = Pink80
        )
    } else {
        lightColorScheme(
            primary = Purple80,
            secondary = PurpleGrey40,
            tertiary = Pink40
        )
    }

    CompositionLocalProvider(LocalAppDimens provides AppDimens()) {
        MaterialTheme(
            colorScheme = colorScheme,
            content = content
        )
    }
}

// Access dimensions
@Composable
fun appDimens() = LocalAppDimens.current