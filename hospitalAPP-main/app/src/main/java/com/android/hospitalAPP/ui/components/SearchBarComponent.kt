// SearchBarComponent.kt
package com.android.hospitalAPP.ui.components

import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.foundation.text.KeyboardActions
import androidx.compose.foundation.text.KeyboardOptions
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.Clear
import androidx.compose.material.icons.filled.Search
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.focus.FocusRequester
import androidx.compose.ui.focus.focusRequester
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.platform.LocalFocusManager
import androidx.compose.ui.text.input.ImeAction
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import com.android.hospitalAPP.ui.theme.SearchBarBackground
import com.android.hospitalAPP.ui.theme.TextSecondary
import com.android.hospitalAPP.ui.theme.appDimens

/**
 * 검색창 컴포넌트
 * @param onSearch 검색 이벤트 핸들러
 * @param placeholder 플레이스홀더 텍스트
 * @param initialQuery 초기 검색어
 * @param modifier 추가 Modifier
 */
@Composable
fun EnhancedSearchBar(
    onSearch: (String) -> Unit,
    placeholder: String = "질병, 진료과, 병원을 검색해보세요.",
    initialQuery: String = "",
    modifier: Modifier = Modifier
) {
    val dimens = appDimens()
    var searchText by remember { mutableStateOf(initialQuery) }
    val focusRequester = remember { FocusRequester() }
    val focusManager = LocalFocusManager.current

    Card(
        modifier = modifier
            .fillMaxWidth()
            .height(52.dp),
        shape = RoundedCornerShape(24.dp),
        colors = CardDefaults.cardColors(containerColor = SearchBarBackground),
        elevation = CardDefaults.cardElevation(0.dp)
    ) {
        Row(
            modifier = Modifier
                .fillMaxSize()
                .padding(horizontal = dimens.paddingLarge.dp),
            verticalAlignment = Alignment.CenterVertically
        ) {
            Icon(
                imageVector = Icons.Default.Search,
                contentDescription = "검색",
                tint = TextSecondary,
                modifier = Modifier.size(dimens.iconSize.dp)
            )

            Spacer(modifier = Modifier.width(dimens.paddingMedium.dp))

            // 검색 입력 필드
            TextField(
                value = searchText,
                onValueChange = { searchText = it },
                modifier = Modifier
                    .weight(1f)
                    .focusRequester(focusRequester),
                placeholder = {
                    Text(
                        text = placeholder,
                        fontSize = 14.sp,
                        color = TextSecondary
                    )
                },
                colors = TextFieldDefaults.colors(
                    focusedContainerColor = Color.Transparent,
                    unfocusedContainerColor = Color.Transparent,
                    disabledContainerColor = Color.Transparent,
                    focusedIndicatorColor = Color.Transparent,
                    unfocusedIndicatorColor = Color.Transparent,
                ),
                singleLine = true,
                maxLines = 1,
                keyboardOptions = KeyboardOptions(imeAction = ImeAction.Search),
                keyboardActions = KeyboardActions(
                    onSearch = {
                        if (searchText.isNotEmpty()) {
                            onSearch(searchText)
                            focusManager.clearFocus()
                        }
                    }
                ),
                trailingIcon = {
                    if (searchText.isNotEmpty()) {
                        Icon(
                            imageVector = Icons.Default.Clear,
                            contentDescription = "지우기",
                            tint = TextSecondary,
                            modifier = Modifier
                                .size(20.dp)
                                .clickable {
                                    searchText = ""
                                    focusRequester.requestFocus()
                                }
                        )
                    }
                }
            )
        }
    }

    // 효과: 초기 검색어가 있다면 자동으로 검색 수행
    LaunchedEffect(initialQuery) {
        if (initialQuery.isNotEmpty()) {
            searchText = initialQuery
            onSearch(initialQuery)
        }
    }
}