package com.example.data.repository

import com.google.firebase.auth.FirebaseAuth
import com.google.firebase.firestore.FirebaseFirestore
import kotlinx.coroutines.tasks.await
import kotlinx.coroutines.flow.Flow
import kotlinx.coroutines.flow.callbackFlow
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.channels.awaitClose
import com.google.firebase.firestore.Query

data class UserProfile(
    val uid: String = "",
    val displayName: String = "",
    val photoUrl: String = ""
)

data class ChatMessage(
    val id: String = "",
    val senderId: String = "",
    val senderName: String = "",
    val text: String = "",
    val timestamp: Long = System.currentTimeMillis()
)

data class Story(
    val id: String = "",
    val userId: String = "",
    val userName: String = "",
    val imageUrl: String = "",
    val timestamp: Long = System.currentTimeMillis()
)

class SocialRepository {
    private val auth = FirebaseAuth.getInstance()
    private val db = FirebaseFirestore.getInstance()

    fun getCurrentUser(): UserProfile? {
        val user = auth.currentUser
        return if (user != null) {
            UserProfile(user.uid, user.displayName ?: "User", user.photoUrl?.toString() ?: "")
        } else null
    }

    suspend fun saveUserProfile() {
        val user = getCurrentUser() ?: return
        db.collection("users").document(user.uid).set(user).await()
    }

    fun getMessages(): Flow<List<ChatMessage>> = callbackFlow {
        val listener = db.collection("messages")
            .orderBy("timestamp", Query.Direction.DESCENDING)
            .limit(50)
            .addSnapshotListener { snapshot, e ->
                if (e != null) {
                    close(e)
                    return@addSnapshotListener
                }
                if (snapshot != null) {
                    val msgs = snapshot.documents.mapNotNull { it.toObject(ChatMessage::class.java) }
                    trySend(msgs)
                }
            }
        awaitClose { listener.remove() }
    }

    fun sendMessage(text: String) {
        val user = getCurrentUser() ?: return
        val ref = db.collection("messages").document()
        val msg = ChatMessage(ref.id, user.uid, user.displayName, text)
        ref.set(msg)
    }

    fun getStories(): Flow<List<Story>> = callbackFlow {
        val listener = db.collection("stories")
            .orderBy("timestamp", Query.Direction.DESCENDING)
            .limit(20)
            .addSnapshotListener { snapshot, e ->
                if (e != null) {
                    close(e)
                    return@addSnapshotListener
                }
                if (snapshot != null) {
                    val stories = snapshot.documents.mapNotNull { it.toObject(Story::class.java) }
                    trySend(stories)
                }
            }
        awaitClose { listener.remove() }
    }

    fun addStory(imageUrl: String) {
        val user = getCurrentUser() ?: return
        val ref = db.collection("stories").document()
        val story = Story(ref.id, user.uid, user.displayName, imageUrl)
        ref.set(story)
    }
}
