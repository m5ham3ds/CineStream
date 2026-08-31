import re

with open("app/src/main/java/com/example/data/repository/SocialRepository.kt", "r") as f:
    content = f.read()

# Modify UserProfile class
user_profile_old = """data class UserProfile(
    val uid: String = "",
    val displayName: String = "",
    val photoUrl: String = "",
    val isOnline: Boolean = false
)"""
user_profile_new = """data class UserProfile(
    val uid: String = "",
    val username: String = "",
    val firstName: String = "",
    val lastName: String = "",
    val photoUrl: String = "",
    val isOnline: Boolean = false
) {
    val displayName: String
        get() = "${firstName} ${lastName}".trim().takeIf { it.isNotBlank() } ?: username
}"""
content = content.replace(user_profile_old, user_profile_new)

# Modify getCurrentUser to use the actual fields
get_current_user_old = """    fun getCurrentUser(): UserProfile? {
        val user = auth.currentUser ?: return null
        return UserProfile(
            uid = user.uid,
            displayName = user.displayName ?: "User",
            photoUrl = user.photoUrl?.toString() ?: "",
            isOnline = true
        )
    }"""
get_current_user_new = """    fun getCurrentUser(): UserProfile? {
        val user = auth.currentUser ?: return null
        // Note: The UI layer (AuthViewModel) is the source of truth for the profile data.
        // For SocialRepository, we'll just return a basic UserProfile.
        return UserProfile(
            uid = user.uid,
            username = "user_${user.uid.take(5)}",
            firstName = user.displayName?.substringBefore(" ") ?: "",
            lastName = user.displayName?.substringAfter(" ", "") ?: "",
            photoUrl = user.photoUrl?.toString() ?: "",
            isOnline = true
        )
    }"""
content = content.replace(get_current_user_old, get_current_user_new)

# Modify search filter
search_filter_old = """val filtered = users.filter { it.displayName.lowercase().contains(lowerQuery) }"""
search_filter_new = """val filtered = users.filter { it.username.lowercase().contains(lowerQuery) || it.displayName.lowercase().contains(lowerQuery) }"""
content = content.replace(search_filter_old, search_filter_new)

# Modify saveUserProfile if it exists
save_user_old = """    suspend fun saveUserProfile() {
        val user = getCurrentUser() ?: return
        db.collection("users").document(user.uid).set(user).await()
    }"""
save_user_new = """    suspend fun saveUserProfile() {
        // We shouldn't overwrite the user profile from SocialRepository
        // because AuthRepository is managing the users collection!
        // We just update the isOnline status.
        val user = auth.currentUser ?: return
        db.collection("users").document(user.uid).update("isOnline", true)
    }"""
content = content.replace(save_user_old, save_user_new)

with open("app/src/main/java/com/example/data/repository/SocialRepository.kt", "w") as f:
    f.write(content)
