import re

with open("app/src/main/java/com/example/ui/screens/profile/ProfileScreen.kt", "r") as f:
    content = f.read()

# Fix signature
content = content.replace("fun ProfileScreen() {", "fun ProfileScreen(onNavigateToAuth: () -> Unit = {}) {")

# Fix sign out button
content = content.replace("onClick = { authViewModel.signOut() }", "onClick = { \n                    authViewModel.signOut()\n                    onNavigateToAuth()\n                }")

# Fix updateProfile call
content = content.replace("authViewModel.updateProfile(firstName, lastName, username) { success, error ->", "authViewModel.updateProfile(firstName, lastName, username, selectedImageUri) { success, error ->")

with open("app/src/main/java/com/example/ui/screens/profile/ProfileScreen.kt", "w") as f:
    f.write(content)
