import re

with open("app/src/main/java/com/example/ui/screens/auth/AuthViewModel.kt", "r") as f:
    content = f.read()

google_signin_old = """                    var existingUser = repository.getCurrentUser()
                    
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
                            kotlinx.coroutines.withTimeoutOrNull(3000) { repository.saveUser(newUser) }
                        } catch (e: Exception) {}
                        _currentUser.value = newUser
                    } else {
                        _currentUser.value = existingUser
                    }"""

google_signin_new = """                    try {
                        val snapshot = kotlinx.coroutines.withTimeout(5000) { com.google.firebase.firestore.FirebaseFirestore.getInstance().collection("users").document(firebaseUser.uid).get().await() }
                        if (snapshot.exists()) {
                            _currentUser.value = snapshot.toObject(User::class.java)
                        } else {
                            val generatedUsername = try { repository.generateUniqueUsername(email?.substringBefore("@") ?: "user") } catch(e:Exception) { "user_" + firebaseUser.uid.take(5) }
                            val newUser = User(
                                uid = firebaseUser.uid,
                                email = email ?: firebaseUser.email ?: "",
                                firstName = displayName?.substringBefore(" ") ?: "",
                                lastName = displayName?.substringAfter(" ", "") ?: "",
                                username = generatedUsername,
                                photoUrl = photoUrl ?: firebaseUser.photoUrl?.toString() ?: ""
                            )
                            kotlinx.coroutines.withTimeoutOrNull(3000) { repository.saveUser(newUser) }
                            _currentUser.value = newUser
                        }
                    } catch (e: Exception) {
                        // Network error or timeout: don't overwrite! Just try to use whatever we can get locally, or wait.
                        _currentUser.value = repository.getCurrentUser() ?: User(uid = firebaseUser.uid, email = firebaseUser.email ?: "")
                        _authError.value = "Warning: Could not sync profile data from server."
                    }"""
                    
email_signin_old = """                    var user = repository.getCurrentUser()
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
                            kotlinx.coroutines.withTimeoutOrNull(3000) { repository.saveUser(user) }
                        } catch (e: Exception) {}
                    }
                    _currentUser.value = user"""

email_signin_new = """                    try {
                        val snapshot = kotlinx.coroutines.withTimeout(5000) { com.google.firebase.firestore.FirebaseFirestore.getInstance().collection("users").document(firebaseUser.uid).get().await() }
                        if (snapshot.exists()) {
                            _currentUser.value = snapshot.toObject(User::class.java)
                        } else {
                            // User document missing? Rare, but create it.
                            val generatedUsername = try { repository.generateUniqueUsername(email.substringBefore("@")) } catch(e:Exception) { "user_" + firebaseUser.uid.take(5) }
                            val user = User(
                                uid = firebaseUser.uid,
                                email = email,
                                firstName = "",
                                lastName = "",
                                username = generatedUsername,
                                photoUrl = ""
                            )
                            kotlinx.coroutines.withTimeoutOrNull(3000) { repository.saveUser(user) }
                            _currentUser.value = user
                        }
                    } catch (e: Exception) {
                        // Network error or timeout. Do NOT overwrite.
                        _currentUser.value = repository.getCurrentUser() ?: User(uid = firebaseUser.uid, email = email)
                        _authError.value = "Warning: Could not sync profile data from server."
                    }"""

content = content.replace(google_signin_old, google_signin_new)
content = content.replace(email_signin_old, email_signin_new)

with open("app/src/main/java/com/example/ui/screens/auth/AuthViewModel.kt", "w") as f:
    f.write(content)
