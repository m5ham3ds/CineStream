package com.example.ui.screens.social

import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import com.example.data.repository.PrivateMessage
import com.example.data.repository.SocialRepository
import com.example.data.repository.UserProfile
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.asStateFlow
import kotlinx.coroutines.launch

class ChatViewModel : ViewModel() {

    private val repo = SocialRepository()

    private val _currentUser = MutableStateFlow<UserProfile?>(repo.getCurrentUser())
    val currentUser: StateFlow<UserProfile?> = _currentUser.asStateFlow()

    private val _otherUser = MutableStateFlow<UserProfile?>(null)
    val otherUser: StateFlow<UserProfile?> = _otherUser.asStateFlow()

    private val _messages = MutableStateFlow<List<PrivateMessage>>(emptyList())
    val messages: StateFlow<List<PrivateMessage>> = _messages.asStateFlow()

    private var currentConversationId: String = ""

    fun loadConversation(conversationId: String) {
        currentConversationId = conversationId
        repo.markConversationAsRead(conversationId)
        
        viewModelScope.launch {
            val conv = repo.getConversation(conversationId)
            if (conv != null) {
                val otherUserId = conv.participants.firstOrNull { it != currentUser.value?.uid }
                if (otherUserId != null) {
                    _otherUser.value = repo.getUserProfile(otherUserId)
                }
            }
        }
        
        viewModelScope.launch {
            repo.getMessages(conversationId).collect { msgs ->
                _messages.value = msgs
                repo.markConversationAsRead(conversationId) // Mark as read as new messages come in
            }
        }
    }

    fun sendMessage(text: String) {
        if (text.isNotBlank() && currentConversationId.isNotEmpty()) {
            repo.sendMessage(currentConversationId, text)
        }
    }
}
