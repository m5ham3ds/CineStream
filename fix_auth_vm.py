import re

with open("app/src/main/java/com/example/ui/screens/auth/AuthViewModel.kt", "r") as f:
    content = f.read()

# Replace handleGoogleSignIn
google_sigin_replacement = """    fun handleGoogleSignIn(idToken: String, email: String?, displayName: String?, photoUrl: String?) {
        viewModelScope.launch {
            _isLoading.value = true
            try {
                val credential = com.google.firebase.auth.GoogleAuthProvider.getCredential(idToken, null)
                val authResult = repository.auth.signInWithCredential(credential).await()
                val firebaseUser = authResult.user
                
                if (firebaseUser != null) {
                    var existingUser = repository.getCurrentUser()
                    
                    if (existingUser == null) {
                        // Try to create new user profile
                        val generatedUsername = try { repository.generateUniqueUsername(email?.substringBefore("@") ?: "user") } catch(e:Exception) { "user_" + firebaseUser.uid.take(5) }
                        val newUser = User(
                            uid = firebaseUser.uid,
                            email = email ?: firebaseUser.email ?: "",
                            firstName = displayName?.substringBefore(" ") ?: "",
                            lastName = displayName?.substringAfter(" ", "") ?: "",
                            username = generatedUsername,
                            photoUrl = photoUrl ?: firebaseUser.photoUrl?.toString() ?: ""
                        )
                        try {
                            repository.saveUser(newUser)
                        } catch (e: Exception) {
                            // Ignore firestore errors and just log them in locally
                        }
                        _currentUser.value = newUser
                    } else {
                        _currentUser.value = existingUser
                    }
                }
            } catch (e: Exception) {
                _authError.value = e.message ?: "Authentication failed"
            } finally {
                _isLoading.value = false
            }
        }
    }"""

content = re.sub(
    r"    fun handleGoogleSignIn\(.*?\).*?_isLoading\.value = false\n            \}\n        \}\n    \}",
    google_sigin_replacement,
    content,
    flags=re.DOTALL
)

# Replace signInWithEmail
email_signin_replacement = """    fun signInWithEmail(email: String, pass: String) {
        viewModelScope.launch {
            _isLoading.value = true
            try {
                val authResult = repository.auth.signInWithEmailAndPassword(email, pass).await()
                val firebaseUser = authResult.user
                if (firebaseUser != null) {
                    var user = repository.getCurrentUser()
                    if (user == null) {
                        val generatedUsername = try { repository.generateUniqueUsername(email.substringBefore("@")) } catch(e:Exception) { "user_" + firebaseUser.uid.take(5) }
                        user = User(
                            uid = firebaseUser.uid,
                            email = email,
                            firstName = "",
                            lastName = "",
                            username = generatedUsername,
                            photoUrl = ""
                        )
                        try {
                            repository.saveUser(user)
                        } catch (e: Exception) {}
                    }
                    _currentUser.value = user
                }
            } catch (e: Exception) {
                _authError.value = e.message ?: "Login failed"
            } finally {
                _isLoading.value = false
            }
        }
    }"""

content = re.sub(
    r"    fun signInWithEmail\(.*?\).*?_isLoading\.value = false\n            \}\n        \}\n    \}",
    email_signin_replacement,
    content,
    flags=re.DOTALL
)

with open("app/src/main/java/com/example/ui/screens/auth/AuthViewModel.kt", "w") as f:
    f.write(content)
