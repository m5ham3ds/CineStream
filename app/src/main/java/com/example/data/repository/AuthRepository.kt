package com.example.data.repository

import android.net.Uri
import com.google.firebase.auth.FirebaseAuth
import com.google.firebase.firestore.FirebaseFirestore
import com.google.firebase.storage.FirebaseStorage
import kotlinx.coroutines.tasks.await

data class User(
    val uid: String = "",
    val email: String = "",
    val firstName: String = "",
    val lastName: String = "",
    val username: String = "",
    val photoUrl: String = ""
)

object AuthRepository {
    val auth: FirebaseAuth = FirebaseAuth.getInstance()
    private val db: FirebaseFirestore = FirebaseFirestore.getInstance()
    private val storage: FirebaseStorage = FirebaseStorage.getInstance()

    suspend fun uploadProfilePicture(uid: String, uri: Uri): String? {
        return try {
            val ref = storage.reference.child("profile_pictures/$uid/${System.currentTimeMillis()}.jpg")
            ref.putFile(uri).await()
            ref.downloadUrl.await().toString()
        } catch (e: Exception) {
            e.printStackTrace()
            null
        }
    }

    suspend fun getCurrentUser(): User? {
        val firebaseUser = auth.currentUser ?: return null
        return try {
            val snapshot = db.collection("users").document(firebaseUser.uid).get().await()
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
