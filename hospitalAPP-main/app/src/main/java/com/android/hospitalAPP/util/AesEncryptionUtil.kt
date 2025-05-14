// AesEncryptionUtil.kt
package com.android.hospitalAPP.util

import android.util.Base64
import java.nio.charset.StandardCharsets
import javax.crypto.Cipher
import javax.crypto.spec.IvParameterSpec
import javax.crypto.spec.SecretKeySpec

/**
 * AES-256 암호화를 위한 유틸리티 클래스
 */
object AesEncryptionUtil {
    // 암호화 키 (32바이트 = 256비트)
    const val SECRET_KEY = "H0sp1t4lAppS3cr3tK3y123456789012" // 실제 배포시 안전하게 관리하세요!

    // 초기화 벡터 (16바이트)
    const val IV = "H0sp1t4lAppIn1tV" // 실제 배포시 안전하게 관리하세요!

    /**
     * AES-256 암호화 메서드
     * @param plainText 암호화할 평문 텍스트
     * @return Base64로 인코딩된 암호화 텍스트
     */
    fun encryptAesBase64(plainText: String): String {
        try {
            val cipher = Cipher.getInstance("AES/CBC/PKCS5Padding")
            val keySpec = SecretKeySpec(SECRET_KEY.toByteArray(), "AES")
            val ivSpec = IvParameterSpec(IV.toByteArray())

            cipher.init(Cipher.ENCRYPT_MODE, keySpec, ivSpec)
            val encrypted = cipher.doFinal(plainText.toByteArray(StandardCharsets.UTF_8))
            return Base64.encodeToString(encrypted, Base64.NO_WRAP)
        } catch (e: Exception) {
            throw RuntimeException("암호화 오류: ${e.message}", e)
        }
    }

    /**
     * AES-256 복호화 메서드
     */
    fun decryptAesBase64(encryptedBase64: String, key: String, iv: String): String {
        val decodedBytes = Base64.decode(encryptedBase64, Base64.NO_WRAP)
        val secretKey = SecretKeySpec(key.toByteArray(Charsets.UTF_8), "AES")
        val ivSpec = IvParameterSpec(iv.toByteArray(Charsets.UTF_8))

        val cipher = Cipher.getInstance("AES/CBC/PKCS5Padding")
        cipher.init(Cipher.DECRYPT_MODE, secretKey, ivSpec)

        val decryptedBytes = cipher.doFinal(decodedBytes)
        return String(decryptedBytes, Charsets.UTF_8)
    }
}