import re
with open("app/src/main/java/com/example/data/repository/AuthRepository.kt", "r") as f:
    content = f.read()

replacement = """    suspend fun getCurrentUser(): User? {
        val firebaseUser = auth.currentUser ?: return null
        return try {
            val snapshot = db.collection("users").document(firebaseUser.uid).get().await()
            if (snapshot.exists()) {
                snapshot.toObject(User::class.java)
            } else {
                null
            }
        } catch (e: Exception) {
            null
        }
    }"""

content = re.sub(
    r"    suspend fun getCurrentUser\(\): User\? \{.*?    \} catch \(e: Exception\) \{\n            User\(\n                uid = firebaseUser\.uid,\n                email = firebaseUser\.email \?: \"\",\n                username = \"user_\" \+ firebaseUser\.uid\.take\(5\)\n            \)\n        \}\n    \}",
    replacement,
    content,
    flags=re.DOTALL
)

with open("app/src/main/java/com/example/data/repository/AuthRepository.kt", "w") as f:
    f.write(content)
