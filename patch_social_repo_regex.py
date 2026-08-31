import re

with open("app/src/main/java/com/example/data/repository/SocialRepository.kt", "r") as f:
    content = f.read()

target = r"""        val listener = db\.collection\("users"\)
            \.whereGreaterThanOrEqualTo\("displayName", query\)
            \.whereLessThanOrEqualTo\("displayName", query \+ "\\uf8ff"\)
            \.addSnapshotListener \{ snapshot, e ->
                if \(e != null\) \{
                    close\(e\)
                    return@addSnapshotListener
                \}
                if \(snapshot != null\) \{
                    val users = snapshot\.documents\.mapNotNull \{ it\.toObject\(UserProfile::class\.java\) \}
                    trySend\(users\)
                \}
            \}"""

replacement = """        val lowerQuery = query.lowercase()
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
            }"""

content = re.sub(target, replacement, content)

with open("app/src/main/java/com/example/data/repository/SocialRepository.kt", "w") as f:
    f.write(content)
