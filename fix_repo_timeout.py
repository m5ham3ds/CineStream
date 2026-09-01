import re

with open("app/src/main/java/com/example/data/repository/AuthRepository.kt", "r") as f:
    content = f.read()

content = content.replace("val snapshot = db.collection(\"users\").document(firebaseUser.uid).get().await()", "val snapshot = kotlinx.coroutines.withTimeout(5000) { db.collection(\"users\").document(firebaseUser.uid).get().await() }")

with open("app/src/main/java/com/example/data/repository/AuthRepository.kt", "w") as f:
    f.write(content)
