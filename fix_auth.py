import re

with open("app/src/main/java/com/example/ui/screens/auth/AuthViewModel.kt", "r") as f:
    content = f.read()

google_signin = """
    fun handleGoogleSignIn(idToken: String, email: String?, displayName: String?, photoUrl: String?) {
        viewModelScope.launch {
            _isLoading.value = true
            try {
                val credential = com.google.firebase.auth.GoogleAuthProvider.getCredential(idToken, null)
                val authResult = repository.auth.signInWithCredential(credential).await()
                val firebaseUser = authResult.user
                
                if (firebaseUser != null) {
                    var existingUser = repository.getCurrentUser()
                    
                    if (existingUser == null) {
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
                        } catch (e: Exception) {}
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
    }
"""

content = content.replace("fun resetError() {\n        _authError.value = null\n    }", "fun resetError() {\n        _authError.value = null\n    }\n" + google_signin)

with open("app/src/main/java/com/example/ui/screens/auth/AuthViewModel.kt", "w") as f:
    f.write(content)
