package com.example.data.repository

import com.google.firebase.auth.FirebaseAuth
import com.google.firebase.firestore.FirebaseFirestore
import com.google.firebase.firestore.Query
import kotlinx.coroutines.channels.awaitClose
import kotlinx.coroutines.flow.Flow
import kotlinx.coroutines.flow.callbackFlow
import kotlinx.coroutines.tasks.await

data class UserProfile(
    val uid: String = "",
    val username: String = "",
    val firstName: String = "",
    val lastName: String = "",
    val photoUrl: String = "",
    val isOnline: Boolean = false,
    val isProfilePublic: Boolean = true
) {
    @get:com.google.firebase.firestore.Exclude
    val displayName: String
        get() = "${firstName} ${lastName}".trim().takeIf { it.isNotBlank() } ?: username
}

data class PrivateMessage(
    val id: String = "",
    val senderId: String = "",
    val text: String = "",
    val timestamp: Long = System.currentTimeMillis()
)

data class Conversation(
    val id: String = "",
    val participants: List<String> = emptyList(),
    val participantNames: Map<String, String> = emptyMap(),
    val lastMessage: String = "",
    val lastMessageTime: Long = 0L,
    val unreadCounts: Map<String, Int> = emptyMap() // Use Int consistently
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
            UserProfile(
                uid = user.uid, 
                username = user.displayName ?: "User", 
                photoUrl = user.photoUrl?.toString() ?: "", 
                isOnline = true
            )
        } else null
    }

    suspend fun saveUserProfile() {
        val user = auth.currentUser ?: return
        try {
            db.collection("users").document(user.uid).update("isOnline", true).await()
        } catch (e: Exception) {
            // Document might not exist yet, ignore
        }
    }
    
    fun searchUsers(query: String): Flow<List<UserProfile>> = callbackFlow {
        if (query.isBlank()) {
            trySend(emptyList())
            return@callbackFlow
        }
        val lowerQuery = query.lowercase()
        val listener = db.collection("users")
            .addSnapshotListener { snapshot, e ->
                if (e != null) {
                    close(e)
                    return@addSnapshotListener
                }
                if (snapshot != null) {
                    val users = snapshot.documents.mapNotNull { it.toObject(UserProfile::class.java) }
                    val filtered = users.filter { 
                        it.isProfilePublic && (it.username.lowercase().contains(lowerQuery) || 
                        it.displayName.lowercase().contains(lowerQuery))
                    }
                    trySend(filtered)
                }
            }
        awaitClose { listener.remove() }
    }

    fun getConversations(): Flow<List<Conversation>> = callbackFlow {
        val user = getCurrentUser()
        if (user == null) {
            trySend(emptyList())
            return@callbackFlow
        }
        
        val listener = db.collection("conversations")
            .whereArrayContains("participants", user.uid)
            .orderBy("lastMessageTime", Query.Direction.DESCENDING)
            .addSnapshotListener { snapshot, e ->
                if (e != null) {
                    close(e)
                    return@addSnapshotListener
                }
                if (snapshot != null) {
                    val convs = snapshot.documents.mapNotNull { it.toObject(Conversation::class.java) }
                    trySend(convs)
                }
            }
        awaitClose { listener.remove() }
    }

    fun getMessages(conversationId: String): Flow<List<PrivateMessage>> = callbackFlow {
        val listener = db.collection("conversations").document(conversationId).collection("messages")
            .orderBy("timestamp", Query.Direction.ASCENDING)
            .addSnapshotListener { snapshot, e ->
                if (e != null) {
                    close(e)
                    return@addSnapshotListener
                }
                if (snapshot != null) {
                    val msgs = snapshot.documents.mapNotNull { it.toObject(PrivateMessage::class.java) }
                    trySend(msgs)
                }
            }
        awaitClose { listener.remove() }
    }
    
    suspend fun startConversation(otherUserId: String, otherUserName: String): String {
        val user = getCurrentUser() ?: return ""
        val dbUserDoc = db.collection("users").document(user.uid).get().await()
        val realUser = dbUserDoc.toObject(UserProfile::class.java) ?: user
        val participants = listOf(user.uid, otherUserId).sorted()
        val convId = participants.joinToString("_")
        
        val docRef = db.collection("conversations").document(convId)
        val doc = docRef.get().await()
        
        if (!doc.exists()) {
            val conv = Conversation(
                id = convId,
                participants = participants,
                participantNames = mapOf(user.uid to realUser.displayName, otherUserId to otherUserName)
            )
            docRef.set(conv).await()
        }
        return convId
    }

    fun sendMessage(conversationId: String, text: String) {
        val user = getCurrentUser() ?: return
        val docRef = db.collection("conversations").document(conversationId)
        
        val msgRef = docRef.collection("messages").document()
        val msg = PrivateMessage(msgRef.id, user.uid, text, System.currentTimeMillis())
        msgRef.set(msg)
        
        db.runTransaction { transaction ->
            val convSnapshot = transaction.get(docRef)
            if (convSnapshot.exists()) {
                val currentCountsAny = convSnapshot.get("unreadCounts")
                val currentCounts = if (currentCountsAny is Map<*, *>) {
                    currentCountsAny.entries.associate { it.key.toString() to (it.value.toString().toIntOrNull() ?: 0) }
                } else emptyMap()
                
                val newCounts = currentCounts.toMutableMap()
                
                val participantsAny = convSnapshot.get("participants")
                val participants = if (participantsAny is List<*>) {
                    participantsAny.map { it.toString() }
                } else emptyList()
                
                for (p in participants) {
                    if (p != user.uid) {
                        newCounts[p] = (newCounts[p] ?: 0) + 1
                    }
                }
                
                transaction.update(docRef, "lastMessage", text)
                transaction.update(docRef, "lastMessageTime", System.currentTimeMillis())
                transaction.update(docRef, "unreadCounts", newCounts)
            }
        }
    }
    
    fun markConversationAsRead(conversationId: String) {
        val user = getCurrentUser() ?: return
        val docRef = db.collection("conversations").document(conversationId)
        
        db.runTransaction { transaction ->
            val convSnapshot = transaction.get(docRef)
            if (convSnapshot.exists()) {
                val currentCountsAny = convSnapshot.get("unreadCounts")
                val currentCounts = if (currentCountsAny is Map<*, *>) {
                    currentCountsAny.entries.associate { it.key.toString() to (it.value.toString().toIntOrNull() ?: 0) }
                } else emptyMap()
                
                val newCounts = currentCounts.toMutableMap()
                newCounts[user.uid] = 0
                
                transaction.update(docRef, "unreadCounts", newCounts)
            }
        }
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
        val story = Story(ref.id, user.uid, user.displayName, imageUrl, System.currentTimeMillis())
        ref.set(story)
    }
}
