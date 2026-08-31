import re

with open("app/src/main/java/com/example/ui/screens/auth/AuthScreen.kt", "r") as f:
    content = f.read()

# Add success toast
success_target = """    LaunchedEffect(currentUser) {
        if (currentUser != null) {
            userPrefs.saveIsGuest(false)
            userPrefs.saveIsLoggedIn(true)
            onAuthSuccess()
        }
    }"""
success_replacement = """    LaunchedEffect(currentUser) {
        if (currentUser != null) {
            android.widget.Toast.makeText(context, "Signed in successfully!", android.widget.Toast.LENGTH_SHORT).show()
            userPrefs.saveIsGuest(false)
            userPrefs.saveIsLoggedIn(true)
            onAuthSuccess()
        }
    }"""
content = content.replace(success_target, success_replacement)

# Update Google Sign in error message
google_target = """Toast.makeText(context, "Google Sign-In not configured", Toast.LENGTH_SHORT).show()"""
google_replacement = """Toast.makeText(context, "Please add WEB_CLIENT_ID to the Secrets panel in AI Studio for Google Sign-In, and ensure SHA-1 is added in Firebase.", Toast.LENGTH_LONG).show()"""
content = content.replace(google_target, google_replacement)

with open("app/src/main/java/com/example/ui/screens/auth/AuthScreen.kt", "w") as f:
    f.write(content)
