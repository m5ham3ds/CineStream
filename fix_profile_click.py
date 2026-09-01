import re

with open("app/src/main/java/com/example/ui/screens/profile/ProfileScreen.kt", "r") as f:
    content = f.read()

content = content.replace(".clickable(enabled = currentUser != null) { showImageConfirmDialog = true }", ".clickable(enabled = currentUser != null) { showEditProfile = true }")

with open("app/src/main/java/com/example/ui/screens/profile/ProfileScreen.kt", "w") as f:
    f.write(content)
