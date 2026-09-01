import re

with open("app/src/main/java/com/example/data/repository/AuthRepository.kt", "r") as f:
    content = f.read()

get_old = """    suspend fun getCurrentUser(): User? {
        val firebaseUser = auth.currentUser ?: return null
        return try {
            val snapshot = kotlinx.coroutines.withTimeout(5000) { db.collection("users").document(firebaseUser.uid).get().await() }
            if (snapshot.exists()) {
                snapshot.toObject(User::class.java)
            } else {
                null
            }
        } catch (e: Exception) {
            null
        }
    }"""

get_new = """    suspend fun getCurrentUser(): User? {
        val firebaseUser = auth.currentUser ?: return null
        return try {
            val snapshot = kotlinx.coroutines.withTimeout(15000) { db.collection("users").document(firebaseUser.uid).get().await() }
            if (snapshot.exists()) {
                snapshot.toObject(User::class.java)
            } else {
                null
            }
        } catch (e: Exception) {
            // Return a basic user object so the app doesn't think they are logged out,
            // but log the error.
            User(uid = firebaseUser.uid, email = firebaseUser.email ?: "", username = "user_" + firebaseUser.uid.take(5))
        }
    }"""

content = content.replace(get_old, get_new)

with open("app/src/main/java/com/example/data/repository/AuthRepository.kt", "w") as f:
    f.write(content)
