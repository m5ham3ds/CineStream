import re

with open("app/src/main/java/com/example/ui/screens/profile/ProfileScreen.kt", "r") as f:
    content = f.read()

content = content.replace("authViewModel.updateProfile(firstName, lastName, username, selectedImageUri)", "authViewModel.updateProfile(firstName, lastName, username, null)")

with open("app/src/main/java/com/example/ui/screens/profile/ProfileScreen.kt", "w") as f:
    f.write(content)
