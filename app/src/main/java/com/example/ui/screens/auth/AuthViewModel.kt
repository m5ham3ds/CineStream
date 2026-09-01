package com.example.ui.screens.auth

import android.net.Uri
import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import com.example.data.repository.AuthRepository
import com.example.data.repository.User
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.asStateFlow
import kotlinx.coroutines.launch
import kotlinx.coroutines.tasks.await

class AuthViewModel : ViewModel() {
    private val repository = AuthRepository
    
    private val _currentUser = MutableStateFlow<User?>(null)
    val currentUser: StateFlow<User?> = _currentUser.asStateFlow()
    
    private val _authError = MutableStateFlow<String?>(null)
    val authError: StateFlow<String?> = _authError.asStateFlow()
    
    private val _isLoading = MutableStateFlow(false)
    val isLoading: StateFlow<Boolean> = _isLoading.asStateFlow()

        init {
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
    }

    fun checkCurrentUser() {
        viewModelScope.launch {
            _isLoading.value = true
            _currentUser.value = repository.getCurrentUser()
            _isLoading.value = false
        }
    }

    fun resetError() {
        _authError.value = null
    }

    fun handleGoogleSignIn(idToken: String, email: String?, displayName: String?, photoUrl: String?) {
        viewModelScope.launch {
            _isLoading.value = true
            try {
                val credential = com.google.firebase.auth.GoogleAuthProvider.getCredential(idToken, null)
                val authResult = kotlinx.coroutines.withTimeout(15000) { repository.auth.signInWithCredential(credential).await() }
                val firebaseUser = authResult.user
                
                if (firebaseUser != null) {
                    try {
                        val snapshot = kotlinx.coroutines.withTimeout(15000) { com.google.firebase.firestore.FirebaseFirestore.getInstance().collection("users").document(firebaseUser.uid).get().await() }
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
                            kotlinx.coroutines.withTimeoutOrNull(15000) { repository.saveUser(newUser) }
                            _currentUser.value = newUser
                        }
                    } catch (e: Exception) {
                        repository.auth.signOut()
                        _authError.value = "Network error: Could not load user profile. Please try again."
                        _currentUser.value = null
                    }
                }
            } catch (e: Exception) {
                _authError.value = e.message ?: "Authentication failed"
            } finally {
                _isLoading.value = false
            }
        }
    }


    fun signInWithEmail(email: String, pass: String) {
        viewModelScope.launch {
            _isLoading.value = true
            try {
                val authResult = kotlinx.coroutines.withTimeout(15000) { repository.auth.signInWithEmailAndPassword(email, pass).await() }
                val firebaseUser = authResult.user
                if (firebaseUser != null) {
                    try {
                        val snapshot = kotlinx.coroutines.withTimeout(15000) { com.google.firebase.firestore.FirebaseFirestore.getInstance().collection("users").document(firebaseUser.uid).get().await() }
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
                            kotlinx.coroutines.withTimeoutOrNull(15000) { repository.saveUser(user) }
                            _currentUser.value = user
                        }
                    } catch (e: Exception) {
                        repository.auth.signOut()
                        _authError.value = "Network error: Could not load user profile. Please try again."
                        _currentUser.value = null
                    }
                }
            } catch (e: Exception) {
                _authError.value = e.message ?: "Login failed"
            } finally {
                _isLoading.value = false
            }
        }
    }

    fun signUpWithEmail(email: String, pass: String) {
        viewModelScope.launch {
            _isLoading.value = true
            try {
                val authResult = kotlinx.coroutines.withTimeout(15000) { repository.auth.createUserWithEmailAndPassword(email, pass).await() }
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
                        kotlinx.coroutines.withTimeout(15000) { repository.saveUser(newUser) }
                    } catch (e: Exception) {}
                    _currentUser.value = newUser
                }
            } catch (e: Exception) {
                _authError.value = e.message ?: "Signup failed"
            } finally {
                _isLoading.value = false
            }
        }
    }

    fun resetPassword(email: String) {
        viewModelScope.launch {
            _isLoading.value = true
            try {
                repository.auth.sendPasswordResetEmail(email).await()
                _authError.value = "Password reset email sent."
            } catch (e: Exception) {
                _authError.value = e.message ?: "Failed to send reset email"
            } finally {
                _isLoading.value = false
            }
        }
    }

    fun updateProfile(firstName: String, lastName: String, username: String, photoUri: Uri? = null, onComplete: (Boolean, String?) -> Unit) {
        val safeUsername = username.lowercase().replace(" ", "").trim()
        viewModelScope.launch {
            _isLoading.value = true
            val currentUserData = _currentUser.value
            if (currentUserData == null) {
                onComplete(false, "User not found")
                _isLoading.value = false
                return@launch
            }
            
            try {
                if (username != currentUserData.username) {
                    val isTaken = repository.isUsernameTaken(safeUsername, currentUserData.uid)
                    if (isTaken) {
                        onComplete(false, "Username is already taken")
                        _isLoading.value = false
                        return@launch
                    }
                }
                
                var finalPhotoUrl = currentUserData.photoUrl
                if (photoUri != null) {
                    val uploadedUrl = repository.uploadProfilePicture(currentUserData.uid, photoUri)
                    if (uploadedUrl != null) {
                        finalPhotoUrl = uploadedUrl
                    } else {
                        onComplete(false, "Failed to upload image. Check Firebase Storage rules or network.")
                        _isLoading.value = false
                        return@launch
                    }
                }
                
                val updatedUser = currentUserData.copy(
                    firstName = firstName,
                    lastName = lastName,
                    username = safeUsername,
                    photoUrl = finalPhotoUrl
                )
                kotlinx.coroutines.withTimeout(15000) { repository.saveUser(updatedUser) }
                _currentUser.value = updatedUser
                onComplete(true, null)
            } catch (e: Exception) {
                onComplete(false, "Failed to save to server. Check connection.")
            } finally {
                _isLoading.value = false
            }
        }
    }

    fun signOut() {
        repository.auth.signOut()
        _currentUser.value = null
    }
}
