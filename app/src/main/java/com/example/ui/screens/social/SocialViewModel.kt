package com.example.ui.screens.social

import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import com.example.data.repository.SocialRepository
import com.example.data.repository.ChatMessage
import com.example.data.repository.Story
import com.example.data.repository.UserProfile
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.asStateFlow
import kotlinx.coroutines.launch

class SocialViewModel : ViewModel() {
    

    private val _currentUser = MutableStateFlow<UserProfile?>(SocialRepository().getCurrentUser())
    val currentUser: StateFlow<UserProfile?> = _currentUser.asStateFlow()

    private val _messages = MutableStateFlow<List<ChatMessage>>(emptyList())
    val messages: StateFlow<List<ChatMessage>> = _messages.asStateFlow()

    private val _stories = MutableStateFlow<List<Story>>(emptyList())
    val stories: StateFlow<List<Story>> = _stories.asStateFlow()

    init {
        com.google.firebase.auth.FirebaseAuth.getInstance().addAuthStateListener { auth ->
            val user = SocialRepository().getCurrentUser()
            _currentUser.value = user
            if (user != null) {
                startListening()
            }
        }
    }

    fun refreshUser() {
        _currentUser.value = SocialRepository().getCurrentUser()
        if (_currentUser.value != null) {
            viewModelScope.launch { SocialRepository().saveUserProfile() }
            startListening()
        }
    }

    private fun startListening() {
        viewModelScope.launch {
            SocialRepository().getMessages().collect { msgs ->
                _messages.value = msgs
            }
        }
        viewModelScope.launch {
            SocialRepository().getStories().collect { sts ->
                _stories.value = sts
            }
        }
    }

    fun sendMessage(text: String) {
        if (text.isNotBlank()) {
            SocialRepository().sendMessage(text)
        }
    }

    fun addStory(imageUrl: String) {
        if (imageUrl.isNotBlank()) {
            SocialRepository().addStory(imageUrl)
        }
    }
}
