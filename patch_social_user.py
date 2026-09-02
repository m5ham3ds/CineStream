import re

with open("app/src/main/java/com/example/data/repository/SocialRepository.kt", "r") as f:
    content = f.read()

old_get_user = """    fun getCurrentUser(): UserProfile? {
        val user = auth.currentUser
        return if (user != null) {
            UserProfile(
                uid = user.uid, 
                username = user.displayName ?: "User", 
                photoUrl = user.photoUrl?.toString() ?: "", 
                isOnline = true
            )
        } else null
    }"""

new_get_user = """    fun getCurrentUser(): UserProfile? {
        val user = com.example.data.repository.AuthRepository.currentUserFlow.value
        return if (user != null) {
            UserProfile(
                uid = user.uid, 
                username = user.username, 
                firstName = user.firstName,
                lastName = user.lastName,
                photoUrl = user.photoUrl, 
                isOnline = true
            )
        } else null
    }"""
content = content.replace(old_get_user, new_get_user)

with open("app/src/main/java/com/example/data/repository/SocialRepository.kt", "w") as f:
    f.write(content)

