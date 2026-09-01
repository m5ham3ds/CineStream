import re

with open("app/src/main/java/com/example/ui/screens/auth/AuthViewModel.kt", "r") as f:
    content = f.read()

content = content.replace("repository.saveUser(user)", "kotlinx.coroutines.withTimeoutOrNull(3000) { repository.saveUser(user) }")
content = content.replace("repository.saveUser(newUser)", "kotlinx.coroutines.withTimeoutOrNull(3000) { repository.saveUser(newUser) }")
content = content.replace("repository.saveUser(updatedUser)", "kotlinx.coroutines.withTimeoutOrNull(3000) { repository.saveUser(updatedUser) }")
content = content.replace("val authResult = repository.auth.signInWithEmailAndPassword(email, pass).await()", "val authResult = kotlinx.coroutines.withTimeout(10000) { repository.auth.signInWithEmailAndPassword(email, pass).await() }")
content = content.replace("val authResult = repository.auth.createUserWithEmailAndPassword(email, pass).await()", "val authResult = kotlinx.coroutines.withTimeout(10000) { repository.auth.createUserWithEmailAndPassword(email, pass).await() }")

with open("app/src/main/java/com/example/ui/screens/auth/AuthViewModel.kt", "w") as f:
    f.write(content)
