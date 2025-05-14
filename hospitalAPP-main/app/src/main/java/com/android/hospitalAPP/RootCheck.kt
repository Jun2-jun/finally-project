package com.android.hospitalAPP

object RootCheck {
    init {
        System.loadLibrary("rootcheck")
    }

    external fun isDeviceRootedNative(): Boolean
}