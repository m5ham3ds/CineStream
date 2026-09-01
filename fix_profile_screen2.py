import re

with open("app/src/main/java/com/example/ui/screens/profile/ProfileScreen.kt", "r") as f:
    content = f.read()

old_call = """                        authViewModel.updateProfile(
                            currentUser?.firstName ?: "", 
                            currentUser?.lastName ?: "", 
                            currentUser?.username ?: "", 
                            selectedImageUri
                        )"""
new_call = """                        authViewModel.updateProfile(
                            currentUser?.firstName ?: "", 
                            currentUser?.lastName ?: "", 
                            currentUser?.username ?: "", 
                            currentUser?.isProfilePublic ?: true,
                            selectedImageUri
                        )"""
content = content.replace(old_call, new_call)

with open("app/src/main/java/com/example/ui/screens/profile/ProfileScreen.kt", "w") as f:
    f.write(content)
