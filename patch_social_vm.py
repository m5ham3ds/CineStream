import re

with open('app/src/main/java/com/example/ui/screens/social/SocialViewModel.kt', 'r') as f:
    content = f.read()

init_block = """
    init {
        com.google.firebase.auth.FirebaseAuth.getInstance().addAuthStateListener { auth ->
            val user = repository.getCurrentUser()
            _currentUser.value = user
            if (user != null) {
                startListening()
            }
        }
    }
"""

content = re.sub(r'    init \{.*?\}', init_block, content, flags=re.DOTALL)

with open('app/src/main/java/com/example/ui/screens/social/SocialViewModel.kt', 'w') as f:
    f.write(content)
