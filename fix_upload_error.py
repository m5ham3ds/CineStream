import re

with open("app/src/main/java/com/example/ui/screens/auth/AuthViewModel.kt", "r") as f:
    content = f.read()

upload_old = """                if (photoUri != null) {
                    val uploadedUrl = repository.uploadProfilePicture(currentUserData.uid, photoUri)
                    if (uploadedUrl != null) {
                        finalPhotoUrl = uploadedUrl
                    }
                }"""

upload_new = """                if (photoUri != null) {
                    val uploadedUrl = repository.uploadProfilePicture(currentUserData.uid, photoUri)
                    if (uploadedUrl != null) {
                        finalPhotoUrl = uploadedUrl
                    } else {
                        onComplete(false, "Failed to upload image. Check Firebase Storage rules or network.")
                        _isLoading.value = false
                        return@launch
                    }
                }"""

content = content.replace(upload_old, upload_new)

with open("app/src/main/java/com/example/ui/screens/auth/AuthViewModel.kt", "w") as f:
    f.write(content)
