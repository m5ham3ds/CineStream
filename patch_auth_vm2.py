import re

with open("app/src/main/java/com/example/ui/screens/auth/AuthViewModel.kt", "r") as f:
    content = f.read()

# Replace currentUser declaration
old_flow = """    private val _currentUser = MutableStateFlow<User?>(null)
    val currentUser: StateFlow<User?> = _currentUser.asStateFlow()"""

new_flow = """    val currentUser: StateFlow<User?> = repository.currentUserFlow"""
content = content.replace(old_flow, new_flow)

# Update checkCurrentUser
old_check = """    fun checkCurrentUser() {
        viewModelScope.launch {
            _isLoading.value = true
            _currentUser.value = repository.getCurrentUser()
            _isLoading.value = false
        }
    }"""
new_check = """    fun checkCurrentUser() {
        viewModelScope.launch {
            _isLoading.value = true
            repository.getCurrentUser()
            _isLoading.value = false
        }
    }"""
content = content.replace(old_check, new_check)

# Update signout
old_signout = """    fun signOut() {
        repository.auth.signOut()
        _currentUser.value = null
    }"""
new_signout = """    fun signOut() {
        repository.auth.signOut()
        viewModelScope.launch { repository.getCurrentUser() }
    }"""
content = content.replace(old_signout, new_signout)

# Update saveUserProfile
content = content.replace("_currentUser.value = updatedUser", "")

# Update init block
old_init = """    init {
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
new_init = """    init {
        repository.auth.addAuthStateListener { auth ->
            viewModelScope.launch {
                val currentAuth = auth.currentUser
                if (currentAuth != null) {
                    if (repository.currentUserFlow.value == null || repository.currentUserFlow.value?.uid != currentAuth.uid) {
                        repository.getCurrentUser()
                    }
                } else {
                    repository.getCurrentUser()
                }
            }
        }
    }"""
content = content.replace(old_init, new_init)

with open("app/src/main/java/com/example/ui/screens/auth/AuthViewModel.kt", "w") as f:
    f.write(content)
