import re

with open("app/src/main/java/com/example/ui/screens/auth/AuthViewModel.kt", "r") as f:
    content = f.read()

content = content.replace("username: String", "username: String")

# Modify updateProfile to lowercase username
update_prof_old = """    fun updateProfile(firstName: String, lastName: String, username: String, photoUri: Uri? = null, onComplete: (Boolean, String?) -> Unit) {"""
update_prof_new = """    fun updateProfile(firstName: String, lastName: String, username: String, photoUri: Uri? = null, onComplete: (Boolean, String?) -> Unit) {
        val safeUsername = username.lowercase().replace(" ", "").trim()"""

content = content.replace(update_prof_old, update_prof_new)
content = content.replace("val isTaken = repository.isUsernameTaken(username, currentUserData.uid)", "val isTaken = repository.isUsernameTaken(safeUsername, currentUserData.uid)")
content = content.replace("username = username,", "username = safeUsername,")

with open("app/src/main/java/com/example/ui/screens/auth/AuthViewModel.kt", "w") as f:
    f.write(content)
