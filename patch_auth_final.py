import re

with open("app/src/main/java/com/example/data/repository/AuthRepository.kt", "r") as f:
    content = f.read()

# Change Flow back to public mutable
old_flow = """    private val _currentUserFlow = MutableStateFlow<User?>(null)
    val currentUserFlow: StateFlow<User?> = _currentUserFlow.asStateFlow()"""
new_flow = """    val currentUserFlow = MutableStateFlow<User?>(null)"""
content = content.replace(old_flow, new_flow)
content = content.replace("_currentUserFlow.value", "currentUserFlow.value")

with open("app/src/main/java/com/example/data/repository/AuthRepository.kt", "w") as f:
    f.write(content)

with open("app/src/main/java/com/example/ui/screens/auth/AuthViewModel.kt", "r") as f:
    content = f.read()

content = content.replace("_currentUser.value", "repository.currentUserFlow.value")
content = content.replace("_currentUser", "repository.currentUserFlow")

with open("app/src/main/java/com/example/ui/screens/auth/AuthViewModel.kt", "w") as f:
    f.write(content)

