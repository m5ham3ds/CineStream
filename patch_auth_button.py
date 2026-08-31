import re

with open("app/src/main/java/com/example/ui/screens/auth/AuthScreen.kt", "r") as f:
    content = f.read()

button_old = """                Button(
                    onClick = {
                        focusManager.clearFocus()
                        keyboardController?.hide()
                        if (email.isNotBlank() && password.isNotBlank()) {"""
button_new = """                Button(
                    onClick = {
                        if (email.isNotBlank() && password.isNotBlank()) {"""
content = content.replace(button_old, button_new)

with open("app/src/main/java/com/example/ui/screens/auth/AuthScreen.kt", "w") as f:
    f.write(content)
