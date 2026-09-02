import re

with open("app/src/main/java/com/example/data/repository/SocialRepository.kt", "r") as f:
    content = f.read()

new_funcs = """    suspend fun getConversation(conversationId: String): Conversation? {
        return try {
            val doc = db.collection("conversations").document(conversationId).get().await()
            doc.toObject(Conversation::class.java)
        } catch (e: Exception) {
            null
        }
    }
    
    suspend fun getUserProfile(userId: String): UserProfile? {
        return try {
            val doc = db.collection("users").document(userId).get().await()
            doc.toObject(UserProfile::class.java)
        } catch (e: Exception) {
            null
        }
    }
"""

# Insert before closing brace of SocialRepository class. Let's insert it before "suspend fun uploadMedia"
content = content.replace("suspend fun uploadMedia", new_funcs + "\n    suspend fun uploadMedia")

with open("app/src/main/java/com/example/data/repository/SocialRepository.kt", "w") as f:
    f.write(content)

