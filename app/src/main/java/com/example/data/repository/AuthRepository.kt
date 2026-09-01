package com.example.data.repository

import android.net.Uri
import com.google.firebase.auth.FirebaseAuth
import com.google.firebase.firestore.FirebaseFirestore
import com.google.firebase.storage.FirebaseStorage
import kotlinx.coroutines.tasks.await
import kotlinx.coroutines.suspendCancellableCoroutine
import kotlin.coroutines.resume
import kotlin.coroutines.resumeWithException

data class User(
    val uid: String = "",
    val email: String = "",
    val firstName: String = "",
    val lastName: String = "",
    val username: String = "",
    val photoUrl: String = "",
    val isProfilePublic: Boolean = true
)

object AuthRepository {
    val auth: FirebaseAuth = FirebaseAuth.getInstance()
    private val db: FirebaseFirestore = FirebaseFirestore.getInstance()
    private val storage: FirebaseStorage = FirebaseStorage.getInstance()

    suspend fun uploadProfilePicture(uid: String, uri: Uri): String {
        val cloudName = com.example.BuildConfig.CLOUDINARY_CLOUD_NAME
        val uploadPreset = com.example.BuildConfig.CLOUDINARY_UPLOAD_PRESET
        
        if (cloudName.isNotEmpty() && uploadPreset.isNotEmpty()) {
            return suspendCancellableCoroutine { continuation ->
                com.cloudinary.android.MediaManager.get().upload(uri)
                    .unsigned(uploadPreset)
                    .callback(object : com.cloudinary.android.callback.UploadCallback {
                        override fun onSuccess(requestId: String?, resultData: Map<*, *>?) {
                            val secureUrl = resultData?.get("secure_url") as? String
                            if (secureUrl != null) {
                                continuation.resume(secureUrl)
                            } else {
                                continuation.resumeWithException(Exception("Secure URL not found"))
                            }
                        }
                        
                        override fun onStart(requestId: String?) {}
                        override fun onProgress(requestId: String?, bytes: Long, totalBytes: Long) {}
                        override fun onError(requestId: String?, error: com.cloudinary.android.callback.ErrorInfo?) {
                            continuation.resumeWithException(Exception(error?.description ?: "Unknown error"))
                        }
                        override fun onReschedule(requestId: String?, error: com.cloudinary.android.callback.ErrorInfo?) {}
                    }).dispatch()
            }
        }
        
        // Fallback to Firebase Storage if Cloudinary is not configured
        val ref = storage.reference.child("profile_pictures/$uid/${System.currentTimeMillis()}.jpg")
        ref.putFile(uri).await()
        return ref.downloadUrl.await().toString()
    }

    suspend fun getCurrentUser(): User? {
        val firebaseUser = auth.currentUser ?: return null
        return try {
            val snapshot = kotlinx.coroutines.withTimeout(15000) { db.collection("users").document(firebaseUser.uid).get().await() }
            if (snapshot.exists()) {
                snapshot.toObject(User::class.java)
            } else {
                null
            }
        } catch (e: Exception) {
            null
        }
    }

    suspend fun saveUser(user: User) {
        db.collection("users").document(user.uid).set(user).await()
    }

    suspend fun isUsernameTaken(username: String, currentUid: String): Boolean {
        val snapshot = db.collection("users")
            .whereEqualTo("username", username)
            .get()
            .await()
            
        for (doc in snapshot.documents) {
            if (doc.id != currentUid) return true
        }
        return false
    }

    suspend fun generateUniqueUsername(baseName: String): String {
        var base = baseName.replace(Regex("[^a-zA-Z0-9]"), "").lowercase()
        if (base.isEmpty()) base = "user"
        
        var attempt = base
        var isTaken = isUsernameTaken(attempt, "")
        var count = 1
        
        while (isTaken) {
            attempt = "${base}${count}"
            isTaken = isUsernameTaken(attempt, "")
            count++
        }
        return attempt
    }
}
