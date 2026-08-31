import re

with open("app/src/main/java/com/example/ui/screens/auth/AuthViewModel.kt", "r") as f:
    content = f.read()

signup_replacement = """    fun signUpWithEmail(email: String, pass: String) {
        viewModelScope.launch {
            _isLoading.value = true
            try {
                val authResult = repository.auth.createUserWithEmailAndPassword(email, pass).await()
                val firebaseUser = authResult.user
                if (firebaseUser != null) {
                    val generatedUsername = try { repository.generateUniqueUsername(email.substringBefore("@")) } catch(e:Exception) { "user_" + firebaseUser.uid.take(5) }
                    val newUser = User(
                        uid = firebaseUser.uid,
                        email = email,
                        firstName = "",
                        lastName = "",
                        username = generatedUsername,
                        photoUrl = ""
                    )
                    try {
                        repository.saveUser(newUser)
                    } catch (e: Exception) {}
                    _currentUser.value = newUser
                }
            } catch (e: Exception) {
                _authError.value = e.message ?: "Signup failed"
            } finally {
                _isLoading.value = false
            }
        }
    }"""

content = re.sub(
    r"    fun signUpWithEmail\(.*?\).*?_isLoading\.value = false\n            \}\n        \}\n    \}",
    signup_replacement,
    content,
    flags=re.DOTALL
)

with open("app/src/main/java/com/example/ui/screens/auth/AuthViewModel.kt", "w") as f:
    f.write(content)
