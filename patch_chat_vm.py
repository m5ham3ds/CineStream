import re

with open("app/src/main/java/com/example/ui/screens/social/ChatViewModel.kt", "r") as f:
    content = f.read()

new_props = """    private val _otherUser = MutableStateFlow<UserProfile?>(null)
    val otherUser: StateFlow<UserProfile?> = _otherUser.asStateFlow()

    private val _messages = MutableStateFlow<List<PrivateMessage>>(emptyList())"""

content = content.replace("    private val _messages = MutableStateFlow<List<PrivateMessage>>(emptyList())", new_props)

load_conv = """    fun loadConversation(conversationId: String) {
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
        
        viewModelScope.launch {"""

content = content.replace("""    fun loadConversation(conversationId: String) {
        currentConversationId = conversationId
        repo.markConversationAsRead(conversationId)
        
        viewModelScope.launch {""", load_conv)

with open("app/src/main/java/com/example/ui/screens/social/ChatViewModel.kt", "w") as f:
    f.write(content)

