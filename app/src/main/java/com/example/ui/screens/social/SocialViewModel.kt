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
    private val repository = SocialRepository()

    private val _currentUser = MutableStateFlow<UserProfile?>(repository.getCurrentUser())
    val currentUser: StateFlow<UserProfile?> = _currentUser.asStateFlow()

    private val _messages = MutableStateFlow<List<ChatMessage>>(emptyList())
    val messages: StateFlow<List<ChatMessage>> = _messages.asStateFlow()

    private val _stories = MutableStateFlow<List<Story>>(emptyList())
    val stories: StateFlow<List<Story>> = _stories.asStateFlow()

    init {
        if (_currentUser.value != null) {
            startListening()
        }
    }

    fun refreshUser() {
        _currentUser.value = repository.getCurrentUser()
        if (_currentUser.value != null) {
            viewModelScope.launch { repository.saveUserProfile() }
            startListening()
        }
    }

    private fun startListening() {
        viewModelScope.launch {
            repository.getMessages().collect { msgs ->
                _messages.value = msgs
            }
        }
        viewModelScope.launch {
            repository.getStories().collect { sts ->
                _stories.value = sts
            }
        }
    }

    fun sendMessage(text: String) {
        if (text.isNotBlank()) {
            repository.sendMessage(text)
        }
    }

    fun addStory(imageUrl: String) {
        if (imageUrl.isNotBlank()) {
            repository.addStory(imageUrl)
        }
    }
}
