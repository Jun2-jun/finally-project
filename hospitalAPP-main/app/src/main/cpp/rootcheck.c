#include <jni.h>
#include <unistd.h>

JNIEXPORT jboolean JNICALL
Java_com_android_hospitalAPP_RootCheck_isDeviceRootedNative(JNIEnv *env, jobject thiz) {
    const char *paths[] = {
            "/system/app/Superuser.apk",
            "/sbin/su",
            "/system/bin/su",
            "/system/xbin/su",
            "/data/local/xbin/su",
            "/data/local/bin/su",
            "/system/sd/xbin/su",
            "/system/bin/failsafe/su",
            "/data/local/su"
    };

    int i;
    for (i = 0; i < sizeof(paths) / sizeof(paths[0]); i++) {
        if (access(paths[i], F_OK) == 0) {
            return JNI_TRUE;  // 루팅 흔적 발견
        }
    }
    return JNI_FALSE;
}