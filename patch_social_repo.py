import re

with open("app/src/main/java/com/example/data/repository/SocialRepository.kt", "r") as f:
    content = f.read()

target = """    fun searchUsers(query: String): Flow<List<UserProfile>> = callbackFlow {
        if (query.isBlank()) {
            trySend(emptyList())
            return@callbackFlow
        }
        val listener = db.collection("users")
            .whereGreaterThanOrEqualTo("displayName", query)
            .whereLessThanOrEqualTo("displayName", query + "\uf8ff")
            .addSnapshotListener { snapshot, e ->
                if (e != null) {
                    close(e)
                    return@addSnapshotListener
                }
                if (snapshot != null) {
                    val users = snapshot.documents.mapNotNull { it.toObject(UserProfile::class.java) }
                    trySend(users)
                }
            }
        awaitClose { listener.remove() }
    }"""

replacement = """    fun searchUsers(query: String): Flow<List<UserProfile>> = callbackFlow {
        if (query.isBlank()) {
            trySend(emptyList())
            return@callbackFlow
        }
        val lowerQuery = query.lowercase()
        val listener = db.collection("users")
            .addSnapshotListener { snapshot, e ->
                if (e != null) {
                    close(e)
                    return@addSnapshotListener
                }
                if (snapshot != null) {
                    val users = snapshot.documents.mapNotNull { it.toObject(UserProfile::class.java) }
                    val filtered = users.filter { it.displayName.lowercase().contains(lowerQuery) || it.username.lowercase().contains(lowerQuery) }
                    trySend(filtered)
                }
            }
        awaitClose { listener.remove() }
    }"""

content = content.replace(target, replacement)

with open("app/src/main/java/com/example/data/repository/SocialRepository.kt", "w") as f:
    f.write(content)

with open("app/src/main/java/com/example/ui/screens/player/PlayerScreen.kt", "r") as f:
    player_content = f.read()

player_content = player_content.replace("package com.example.ui.screens.player", "package com.example.ui.screens.player\n\n@file:OptIn(androidx.compose.material3.ExperimentalMaterial3Api::class)\n")

with open("app/src/main/java/com/example/ui/screens/player/PlayerScreen.kt", "w") as f:
    f.write(player_content)
