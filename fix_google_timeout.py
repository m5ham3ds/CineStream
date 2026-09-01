import re

with open("app/src/main/java/com/example/ui/screens/auth/AuthViewModel.kt", "r") as f:
    content = f.read()

content = content.replace("val authResult = repository.auth.signInWithCredential(credential).await()", "val authResult = kotlinx.coroutines.withTimeout(10000) { repository.auth.signInWithCredential(credential).await() }")
with open("app/src/main/java/com/example/ui/screens/auth/AuthViewModel.kt", "w") as f:
    f.write(content)
