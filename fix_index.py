import re

with open("app/src/main/java/com/example/data/repository/SocialRepository.kt", "r") as f:
    content = f.read()

old_query = """        val listener = db.collection("conversations")
            .whereArrayContains("participants", user.uid)
            .orderBy("lastMessageTime", Query.Direction.DESCENDING)
            .addSnapshotListener { snapshot, e ->
                if (e != null) {
                    close(e)
                    return@addSnapshotListener
                }
                if (snapshot != null) {
                    val convs = snapshot.documents.mapNotNull { it.toObject(Conversation::class.java) }
                    trySend(convs)
                }
            }"""

new_query = """        val listener = db.collection("conversations")
            .whereArrayContains("participants", user.uid)
            .addSnapshotListener { snapshot, e ->
                if (e != null) {
                    close(e)
                    return@addSnapshotListener
                }
                if (snapshot != null) {
                    val convs = snapshot.documents.mapNotNull { it.toObject(Conversation::class.java) }
                        .sortedByDescending { it.lastMessageTime }
                    trySend(convs)
                }
            }"""

if old_query in content:
    content = content.replace(old_query, new_query)
    with open("app/src/main/java/com/example/data/repository/SocialRepository.kt", "w") as f:
        f.write(content)
    print("Success")
else:
    print("Not found")

