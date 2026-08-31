package com.example.ui.screens.social

import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import com.example.data.repository.*
import kotlinx.coroutines.Job
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.asStateFlow
import kotlinx.coroutines.launch

class SocialViewModel : ViewModel() {

    private val repo = SocialRepository()

    private val _currentUser = MutableStateFlow<UserProfile?>(repo.getCurrentUser())
    val currentUser: StateFlow<UserProfile?> = _currentUser.asStateFlow()

    private val _conversations = MutableStateFlow<List<Conversation>>(emptyList())
    val conversations: StateFlow<List<Conversation>> = _conversations.asStateFlow()

    private val _stories = MutableStateFlow<List<Story>>(emptyList())
    val stories: StateFlow<List<Story>> = _stories.asStateFlow()
    
    private val _searchResults = MutableStateFlow<List<UserProfile>>(emptyList())
    val searchResults: StateFlow<List<UserProfile>> = _searchResults.asStateFlow()

    private var searchJob: Job? = null

    init {
        com.google.firebase.auth.FirebaseAuth.getInstance().addAuthStateListener { auth ->
            val user = repo.getCurrentUser()
            _currentUser.value = user
            if (user != null) {
                startListening()
            }
        }
    }

    fun refreshUser() {
        _currentUser.value = repo.getCurrentUser()
        if (_currentUser.value != null) {
            viewModelScope.launch { repo.saveUserProfile() }
            startListening()
        }
    }

    private fun startListening() {
        viewModelScope.launch {
            repo.getConversations().collect { convs ->
                _conversations.value = convs
            }
        }
        viewModelScope.launch {
            repo.getStories().collect { sts ->
                _stories.value = sts
            }
        }
    }
    
    fun searchUsers(query: String) {
        searchJob?.cancel()
        if (query.isBlank()) {
            _searchResults.value = emptyList()
            return
        }
        searchJob = viewModelScope.launch {
            repo.searchUsers(query).collect { users ->
                _searchResults.value = users
            }
        }
    }
    
    fun startConversation(otherUserId: String, otherUserName: String, onConversationStarted: (String) -> Unit) {
        viewModelScope.launch {
            val convId = repo.startConversation(otherUserId, otherUserName)
            if (convId.isNotEmpty()) {
                onConversationStarted(convId)
            }
        }
    }

    fun addStory(imageUrl: String) {
        if (imageUrl.isNotBlank()) {
            repo.addStory(imageUrl)
        }
    }
}
