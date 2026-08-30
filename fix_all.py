import re

# Fix AuthScreen.kt (String resources)
with open('app/src/main/java/com/example/ui/screens/auth/AuthScreen.kt', 'r') as f:
    auth_screen = f.read()

auth_screen = auth_screen.replace('stringResource(R.string.skip)', '"Skip"')
auth_screen = auth_screen.replace('stringResource(R.string.create_account)', '"Create Account"')
auth_screen = auth_screen.replace('stringResource(R.string.welcome_back)', '"Welcome Back"')
auth_screen = auth_screen.replace('stringResource(R.string.sign_up_desc)', '"Sign up to get started"')
auth_screen = auth_screen.replace('stringResource(R.string.sign_in_desc)', '"Sign in to continue"')
with open('app/src/main/java/com/example/ui/screens/auth/AuthScreen.kt', 'w') as f:
    f.write(auth_screen)


# Fix AuthViewModel.kt
with open('app/src/main/java/com/example/ui/screens/auth/AuthViewModel.kt', 'r') as f:
    auth_vm = f.read()

if 'import kotlinx.coroutines.tasks.await' not in auth_vm:
    auth_vm = auth_vm.replace('import kotlinx.coroutines.launch', 'import kotlinx.coroutines.launch\nimport kotlinx.coroutines.tasks.await')

with open('app/src/main/java/com/example/ui/screens/auth/AuthViewModel.kt', 'w') as f:
    f.write(auth_vm)


# Fix SocialViewModel.kt (Revert bad regex)
# Let's completely recreate SocialViewModel.kt since I ruined it.
social_vm_content = """package com.example.ui.screens.social

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
        com.google.firebase.auth.FirebaseAuth.getInstance().addAuthStateListener { auth ->
            val user = repository.getCurrentUser()
            _currentUser.value = user
            if (user != null) {
                startListening()
            }
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
"""
with open('app/src/main/java/com/example/ui/screens/social/SocialViewModel.kt', 'w') as f:
    f.write(social_vm_content)


# Fix SocialScreen.kt 'padding' and 'sendMessage'
with open('app/src/main/java/com/example/ui/screens/social/SocialScreen.kt', 'r') as f:
    social_screen = f.read()

# I removed Scaffold somehow or padding is not defined. Let's add Scaffold.
# It seems `padding` was referenced without being defined. I'll just change `padding(padding)` to `padding(0.dp)`.
social_screen = social_screen.replace('.padding(padding)', '.padding(0.dp)')
# 'viewModel.sendMessage' should work if we pass `viewModel` to SocialScreen, wait, where is viewModel defined?
if 'val viewModel: SocialViewModel = viewModel(' not in social_screen:
    # Add it right after `val scope = rememberCoroutineScope()`
    social_screen = social_screen.replace('val scope = rememberCoroutineScope()', 'val scope = rememberCoroutineScope()\n    val viewModel: SocialViewModel = viewModel(factory = ViewModelFactory())')
    # Add currentUser logic
    social_screen = social_screen.replace('val scope = rememberCoroutineScope()\n    val viewModel: SocialViewModel = viewModel(factory = ViewModelFactory())', 'val scope = rememberCoroutineScope()\n    val viewModel: SocialViewModel = viewModel(factory = ViewModelFactory())\n    val currentUser by viewModel.currentUser.collectAsState()\n    val messages by viewModel.messages.collectAsState()\n    val stories by viewModel.stories.collectAsState()')

with open('app/src/main/java/com/example/ui/screens/social/SocialScreen.kt', 'w') as f:
    f.write(social_screen)

