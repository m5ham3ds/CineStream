import re

with open("app/src/main/java/com/example/ui/screens/profile/ProfileScreen.kt", "r") as f:
    content = f.read()

# Replace the function signature
content = content.replace("fun ProfileScreen(onNavigateToAuth: () -> Unit = {}) {", "fun ProfileScreen(onNavigateToAuth: () -> Unit = {}, onNavigateToEditProfile: () -> Unit = {}) {")

# Remove AlertDialog. We'll use a regex to match the `if (showEditProfile && currentUser != null) { ... }` block.
# Or just replace the boolean check to `false` and we can leave the code, but better to remove it.
# Wait, it's easier to just replace `showEditProfile = true` with `onNavigateToEditProfile()`.

content = content.replace(".clickable(enabled = currentUser != null) { showEditProfile = true }", ".clickable(enabled = currentUser != null) { onNavigateToEditProfile() }")

with open("app/src/main/java/com/example/ui/screens/profile/ProfileScreen.kt", "w") as f:
    f.write(content)

