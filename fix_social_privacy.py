import re

with open("app/src/main/java/com/example/data/repository/SocialRepository.kt", "r") as f:
    content = f.read()

old_user = """data class UserProfile(
    val uid: String = "",
    val username: String = "",
    val firstName: String = "",
    val lastName: String = "",
    val photoUrl: String = "",
    val isOnline: Boolean = false
)"""
new_user = """data class UserProfile(
    val uid: String = "",
    val username: String = "",
    val firstName: String = "",
    val lastName: String = "",
    val photoUrl: String = "",
    val isOnline: Boolean = false,
    val isProfilePublic: Boolean = true
)"""
content = content.replace(old_user, new_user)

# Update searchUsers to filter out private profiles!
old_search = """                if (snapshot != null) {
                    val users = snapshot.documents.mapNotNull { it.toObject(UserProfile::class.java) }
                    val filtered = users.filter { 
                        it.username.lowercase().contains(lowerQuery) || 
                        it.displayName.lowercase().contains(lowerQuery) 
                    }
                    trySend(filtered)
                }"""
new_search = """                if (snapshot != null) {
                    val users = snapshot.documents.mapNotNull { it.toObject(UserProfile::class.java) }
                    val filtered = users.filter { 
                        it.isProfilePublic && (it.username.lowercase().contains(lowerQuery) || 
                        it.displayName.lowercase().contains(lowerQuery))
                    }
                    trySend(filtered)
                }"""
content = content.replace(old_search, new_search)

# Update getCurrentUser() to get the displayName and photoUrl properly if it's missing, but it's synchronous so we can't fetch from DB here easily.
# We'll leave getCurrentUser as is, but we can fix startConversation to fetch the current user's name from DB if it exists!

old_start_conv = """    suspend fun startConversation(otherUserId: String, otherUserName: String): String {
        val user = getCurrentUser() ?: return ""
        val participants = listOf(user.uid, otherUserId).sorted()"""
new_start_conv = """    suspend fun startConversation(otherUserId: String, otherUserName: String): String {
        val user = getCurrentUser() ?: return ""
        val dbUserDoc = db.collection("users").document(user.uid).get().await()
        val realUser = dbUserDoc.toObject(UserProfile::class.java) ?: user
        val participants = listOf(user.uid, otherUserId).sorted()"""
content = content.replace(old_start_conv, new_start_conv)

old_start_conv2 = """participantNames = mapOf(user.uid to user.displayName, otherUserId to otherUserName)"""
new_start_conv2 = """participantNames = mapOf(user.uid to realUser.displayName, otherUserId to otherUserName)"""
content = content.replace(old_start_conv2, new_start_conv2)

with open("app/src/main/java/com/example/data/repository/SocialRepository.kt", "w") as f:
    f.write(content)
