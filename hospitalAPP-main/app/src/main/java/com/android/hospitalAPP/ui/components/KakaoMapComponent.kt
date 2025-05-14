package com.android.hospitalAPP.ui.components

import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.runtime.Composable
import androidx.compose.runtime.DisposableEffect
import androidx.compose.runtime.LaunchedEffect
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.setValue
import androidx.compose.ui.Modifier
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.platform.LocalLifecycleOwner
import androidx.compose.ui.viewinterop.AndroidView
import androidx.lifecycle.Lifecycle
import androidx.lifecycle.LifecycleEventObserver
import com.android.hospitalAPP.data.PlaceSearchResult
import com.kakao.vectormap.KakaoMap
import com.kakao.vectormap.KakaoMapReadyCallback
import com.kakao.vectormap.LatLng
import com.kakao.vectormap.MapLifeCycleCallback
import com.kakao.vectormap.MapView
import com.kakao.vectormap.camera.CameraAnimation
import com.kakao.vectormap.camera.CameraUpdateFactory
import com.kakao.vectormap.label.LabelLayer
import com.kakao.vectormap.label.LabelLayerOptions
import com.kakao.vectormap.label.LabelOptions
import com.kakao.vectormap.label.LabelStyle
import com.kakao.vectormap.label.LabelStyles
import java.util.UUID
import com.android.hospitalAPP.R
import com.kakao.vectormap.label.OrderingType

@Composable
fun KakaoMapView(
    places: List<PlaceSearchResult> = emptyList(),
    selectedPlace: PlaceSearchResult? = null,
    onMapClick: () -> Unit = {},
    onMarkerClick: (PlaceSearchResult) -> Unit = {}
) {
    val context = LocalContext.current
    val mapView = remember { MapView(context) }
    val lifecycleOwner = LocalLifecycleOwner.current

    val mapState = remember { MapState() }
    var isMapReady by remember { mutableStateOf(false) }

    DisposableEffect(lifecycleOwner) {
        val observer = LifecycleEventObserver { _, event ->
            when (event) {
                Lifecycle.Event.ON_RESUME -> mapView.resume()
                Lifecycle.Event.ON_PAUSE -> mapView.pause()
                Lifecycle.Event.ON_DESTROY -> mapView.finish()
                else -> {}
            }
        }
        lifecycleOwner.lifecycle.addObserver(observer)
        onDispose {
            lifecycleOwner.lifecycle.removeObserver(observer)
        }
    }

    Box(modifier = Modifier.fillMaxSize()) {
        AndroidView(
            factory = {
                mapView.apply {
                    start(object : MapLifeCycleCallback() {
                        override fun onMapDestroy() {}
                        override fun onMapError(error: Exception?) {}
                    }, object : KakaoMapReadyCallback() {
                        override fun onMapReady(kakaoMap: KakaoMap) {
                            mapState.map = kakaoMap

                            kakaoMap.labelManager?.let { labelManager ->
                                // 마커 스타일 설정 - 앵커 포인트 설정
                                val defaultStyle = LabelStyle.from(R.drawable.ic_marker)
                                    .setAnchorPoint(0.5f, 1.0f)  // 마커의 아래쪽 중앙이 위치 좌표에 오도록 설정

                                labelManager.addLabelStyles(LabelStyles.from("defaultStyle", defaultStyle))

                                val layerOptions = LabelLayerOptions.from("marker_layer")
                                    .setOrderingType(OrderingType.Rank)
                                    .setZOrder(1)

                                mapState.labelLayer = labelManager.addLayer(layerOptions)
                            }

                            val initialPosition = LatLng.from(37.566826, 126.9786567)
                            val cameraUpdate =
                                CameraUpdateFactory.newCenterPosition(initialPosition, 12)
                            kakaoMap.moveCamera(cameraUpdate)

                            isMapReady = true
                        }
                    })
                }
                mapView
            }
        )
    }

    LaunchedEffect(isMapReady, places) {
        if (!isMapReady || mapState.labelLayer == null) return@LaunchedEffect

        try {
            mapState.labelLayer?.removeAll()
            mapState.markerMap.clear()

            places.forEach { place ->
                try {
                    val position = LatLng.from(place.latitude, place.longitude)
                    val labelId = UUID.randomUUID().toString()

                    // 마커 생성
                    val labelOptions = LabelOptions.from(labelId, position).apply {
                        styles = mapState.map?.labelManager?.getLabelStyles("defaultStyle")
                        setRank(1)
                        setVisible(true)
                    }

                    mapState.labelLayer?.addLabel(labelOptions)?.let { label ->
                        // 라벨 크기 조절 - 10%로 축소
                        label.scaleTo(0.1f, 0.1f)
                        label.show()

                        // 클릭 이벤트 처리를 위해 라벨과 장소 정보 매핑
                        mapState.markerMap[labelId] = place
                    }
                } catch (e: Exception) {
                    // 예외 처리
                }
            }
        } catch (e: Exception) {
            // 예외 처리
        }
    }

    LaunchedEffect(selectedPlace) {
        if (!isMapReady || selectedPlace == null) return@LaunchedEffect

        try {
            val position = LatLng.from(selectedPlace.latitude, selectedPlace.longitude)
            val cameraUpdate = CameraUpdateFactory.newCenterPosition(position, 15)
            mapState.map?.moveCamera(cameraUpdate, CameraAnimation.from(300))
        } catch (e: Exception) {
            // 예외 처리
        }
    }
}

private class MapState {
    var map: KakaoMap? = null
    var labelLayer: LabelLayer? = null
    val markerMap = mutableMapOf<String, PlaceSearchResult>()
}