package com.android.hospitalAPP.util

import android.content.Context
import android.content.SharedPreferences
import org.json.JSONObject
import com.android.hospitalAPP.data.Patient

/**
 * SharedPreferences를 관리하는 유틸리티 클래스
 */
class SharedPreferencesManager(context: Context) {
    private val prefs: SharedPreferences = context.getSharedPreferences(PREF_NAME, Context.MODE_PRIVATE)
    private val editor: SharedPreferences.Editor = prefs.edit()

    /**
     * 자동 로그인 정보 저장
     */
    fun saveLoginInfo(userId: String, password: String, rememberMe: Boolean) {
        editor.putString(KEY_USER_ID, userId)
        editor.putString(KEY_PASSWORD, password)
        editor.putBoolean(KEY_REMEMBER_ME, rememberMe)
        editor.apply()
    }

    /**
     * 자동 로그인 상태 확인
     */
    fun isAutoLoginEnabled(): Boolean {
        return prefs.getBoolean(KEY_REMEMBER_ME, false)
    }

    /**
     * 저장된 사용자 ID 반환
     */
    fun getUserId(): String {
        return prefs.getString(KEY_USER_ID, "") ?: ""
    }

    /**
     * 저장된 비밀번호 반환
     */
    fun getPassword(): String {
        return prefs.getString(KEY_PASSWORD, "") ?: ""
    }

    /**
     * 세션 ID 저장
     */
    fun saveSessionId(sessionId: String) {
        editor.putString(KEY_SESSION_ID, sessionId)
        editor.apply()
    }

    /**
     * 저장된 세션 ID 반환
     */
    fun getSessionId(): String {
        return prefs.getString(KEY_SESSION_ID, "") ?: ""
    }

    /**
     * 로그인 정보 모두 삭제 (로그아웃 시 호출)
     */
    fun clearLoginInfo() {
        if (!isAutoLoginEnabled()) {
            // 자동 로그인이 비활성화된 경우에만 모든 정보 삭제
            editor.remove(KEY_USER_ID)
            editor.remove(KEY_PASSWORD)
        }
        editor.remove(KEY_SESSION_ID)
        editor.apply()
    }

    fun savePatientInfo(patient: Patient) {
        val json = JSONObject().apply {
            put("blood_type", patient.bloodType)
            put("height_cm", patient.heightCm)
            put("weight_kg", patient.weightKg)
            put("allergy_info", patient.allergyInfo)
            put("past_illnesses", patient.pastIllnesses)
            put("chronic_diseases", patient.chronicDiseases)
        }
        prefs.edit().putString("patient_info", json.toString()).apply()
    }

    /**
     * 모든 정보 삭제
     */
    fun clearAll() {
        editor.clear()
        editor.apply()
    }

    companion object {
        private const val PREF_NAME = "hospital_app_prefs"
        private const val KEY_USER_ID = "user_id"
        private const val KEY_PASSWORD = "password"
        private const val KEY_REMEMBER_ME = "remember_me"
        private const val KEY_SESSION_ID = "session_id"

        // 싱글톤 인스턴스
        @Volatile
        private var instance: SharedPreferencesManager? = null

        fun getInstance(context: Context): SharedPreferencesManager {
            return instance ?: synchronized(this) {
                instance ?: SharedPreferencesManager(context.applicationContext).also { instance = it }
            }
        }
    }
}