package com.example.ui.screens.auth

import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import com.example.data.repository.AuthRepository
import com.example.data.repository.User
import android.net.Uri
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
    }

    fun signInWithEmail(email: String, pass: String) {
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
    }

    fun signUpWithEmail(email: String, pass: String) {
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
        viewModelScope.launch {
            _isLoading.value = true
            val currentUser = _currentUser.value
            if (currentUser == null) {
                onComplete(false, "User not found")
                _isLoading.value = false
                return@launch
            }
            
            try {
                if (username != currentUser.username) {
                    val isTaken = repository.isUsernameTaken(username, currentUser.uid)
                    if (isTaken) {
                        onComplete(false, "Username is already taken")
                        _isLoading.value = false
                        return@launch
                    }
                }
                
                var finalPhotoUrl = currentUser.photoUrl
                if (photoUri != null) {
                    val uploadedUrl = repository.uploadProfilePicture(currentUser.uid, photoUri)
                    if (uploadedUrl != null) {
                        finalPhotoUrl = uploadedUrl
                    }
                }
                
                val updatedUser = currentUser.copy(
                    firstName = firstName,
                    lastName = lastName,
                    username = username,
                    photoUrl = finalPhotoUrl
                )
                repository.saveUser(updatedUser)
                _currentUser.value = updatedUser
                onComplete(true, null)
            } catch (e: Exception) {
                onComplete(false, e.message)
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
