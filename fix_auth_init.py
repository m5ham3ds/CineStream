import re

with open("app/src/main/java/com/example/ui/screens/auth/AuthViewModel.kt", "r") as f:
    content = f.read()

new_init = """    init {
        repository.auth.addAuthStateListener { auth ->
            viewModelScope.launch {
                val currentAuth = auth.currentUser
                if (currentAuth != null) {
                    if (_currentUser.value == null || _currentUser.value?.uid != currentAuth.uid) {
                        val fetchedUser = repository.getCurrentUser()
                        if (fetchedUser != null) {
                            _currentUser.value = fetchedUser
                        }
                    }
                } else {
                    _currentUser.value = null
                }
            }
        }
    }"""

content = re.sub(r'init\s*\{[\s\S]*?\}\n\s*\}\n\n', new_init + '\n\n', content)

with open("app/src/main/java/com/example/ui/screens/auth/AuthViewModel.kt", "w") as f:
    f.write(content)
