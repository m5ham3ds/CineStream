import re

with open("app/src/main/java/com/example/ui/screens/social/SocialViewModel.kt", "r") as f:
    content = f.read()

new_init = """    init {
        viewModelScope.launch {
            AuthRepository.currentUserFlow.collect { authUser ->
                if (authUser != null) {
                    _currentUser.value = UserProfile(
                        uid = authUser.uid,
                        username = authUser.username,
                        firstName = authUser.firstName,
                        lastName = authUser.lastName,
                        photoUrl = authUser.photoUrl,
                        isOnline = true,
                        isProfilePublic = authUser.isProfilePublic
                    )
                    startListening()
                } else {
                    _currentUser.value = null
                    stopListening()
                }
            }
        }
    }"""
content = re.sub(r"    init \{.*?    \}", new_init, content, flags=re.DOTALL)

with open("app/src/main/java/com/example/ui/screens/social/SocialViewModel.kt", "w") as f:
    f.write(content)

