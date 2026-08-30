import re

with open('app/src/main/java/com/example/ui/screens/auth/AuthViewModel.kt', 'r') as f:
    content = f.read()

init_block = """
    init {
        repository.auth.addAuthStateListener { auth ->
            viewModelScope.launch {
                _isLoading.value = true
                if (auth.currentUser != null) {
                    _currentUser.value = repository.getCurrentUser()
                } else {
                    _currentUser.value = null
                }
                _isLoading.value = false
            }
        }
    }
"""

content = re.sub(r'    init \{.*?\}', init_block, content, flags=re.DOTALL)

with open('app/src/main/java/com/example/ui/screens/auth/AuthViewModel.kt', 'w') as f:
    f.write(content)
