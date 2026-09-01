import re

with open("app/src/main/java/com/example/ui/screens/auth/AuthViewModel.kt", "r") as f:
    content = f.read()

# Replace updateProfile signature
content = content.replace(
    "fun updateProfile(firstName: String, lastName: String, username: String, photoUri: Uri? = null, onComplete: (Boolean, String?) -> Unit) {",
    "fun updateProfile(firstName: String, lastName: String, username: String, isProfilePublic: Boolean = true, photoUri: Uri? = null, onComplete: (Boolean, String?) -> Unit) {"
)

# I also need to check the copy function again.
old_copy = """                val updatedUser = currentUserData.copy(
                    firstName = firstName,
                    lastName = lastName,
                    username = safeUsername,
                    photoUrl = finalPhotoUrl
                )"""
new_copy = """                val updatedUser = currentUserData.copy(
                    firstName = firstName,
                    lastName = lastName,
                    username = safeUsername,
                    photoUrl = finalPhotoUrl,
                    isProfilePublic = isProfilePublic
                )"""
if old_copy in content:
    content = content.replace(old_copy, new_copy)

with open("app/src/main/java/com/example/ui/screens/auth/AuthViewModel.kt", "w") as f:
    f.write(content)
