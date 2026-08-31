import re

with open("app/src/main/java/com/example/ui/screens/auth/AuthViewModel.kt", "r") as f:
    content = f.read()

# Add android.net.Uri import
content = content.replace("import com.example.data.repository.User", "import com.example.data.repository.User\nimport android.net.Uri")

# Modify updateProfile to take optional photoUri
old_update_profile = """    fun updateProfile(firstName: String, lastName: String, username: String, onComplete: (Boolean, String?) -> Unit) {"""
new_update_profile = """    fun updateProfile(firstName: String, lastName: String, username: String, photoUri: Uri? = null, onComplete: (Boolean, String?) -> Unit) {"""
content = content.replace(old_update_profile, new_update_profile)

# Modify updateProfile logic to handle photo upload
old_logic = """                val updatedUser = currentUser.copy(
                    firstName = firstName,
                    lastName = lastName,
                    username = username
                )"""
new_logic = """                var finalPhotoUrl = currentUser.photoUrl
                if (photoUri != null) {
                    val uploadedUrl = repository.uploadProfilePicture(currentUser.uid, photoUri)
                    if (uploadedUrl != null) {
                        finalPhotoUrl = uploadedUrl
                    }
                }
                
                val updatedUser = currentUser.copy(
                    firstName = firstName,
                    lastName = lastName,
                    username = username,
                    photoUrl = finalPhotoUrl
                )"""
content = content.replace(old_logic, new_logic)

with open("app/src/main/java/com/example/ui/screens/auth/AuthViewModel.kt", "w") as f:
    f.write(content)
