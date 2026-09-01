import re

with open("app/src/main/java/com/example/data/repository/SocialRepository.kt", "r") as f:
    content = f.read()

# Replace val displayName with @get:Exclude
old_profile = """data class UserProfile(
    val uid: String = "",
    val username: String = "",
    val firstName: String = "",
    val lastName: String = "",
    val photoUrl: String = "",
    val isOnline: Boolean = false,
    val isProfilePublic: Boolean = true
) {
    val displayName: String
        get() = "${firstName} ${lastName}".trim().takeIf { it.isNotBlank() } ?: username
}"""

new_profile = """data class UserProfile(
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
}"""

content = content.replace(old_profile, new_profile)

with open("app/src/main/java/com/example/data/repository/SocialRepository.kt", "w") as f:
    f.write(content)
