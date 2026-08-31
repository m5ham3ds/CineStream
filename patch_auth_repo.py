import re

with open("app/src/main/java/com/example/data/repository/AuthRepository.kt", "r") as f:
    content = f.read()

# Add FirebaseStorage import
content = content.replace("import com.google.firebase.firestore.FirebaseFirestore", "import com.google.firebase.firestore.FirebaseFirestore\nimport com.google.firebase.storage.FirebaseStorage\nimport android.net.Uri")

# Add FirebaseStorage instance
content = content.replace("private val db = FirebaseFirestore.getInstance()", "private val db = FirebaseFirestore.getInstance()\n    private val storage = FirebaseStorage.getInstance()")

# Add uploadProfilePicture method
upload_method = """
    suspend fun uploadProfilePicture(uid: String, uri: Uri): String? {
        return try {
            val ref = storage.reference.child("profile_pictures/$uid.jpg")
            ref.putFile(uri).await()
            ref.downloadUrl.await().toString()
        } catch (e: Exception) {
            e.printStackTrace()
            null
        }
    }
"""

content = content.replace("suspend fun getCurrentUser(): User? {", upload_method + "\n    suspend fun getCurrentUser(): User? {")

with open("app/src/main/java/com/example/data/repository/AuthRepository.kt", "w") as f:
    f.write(content)
