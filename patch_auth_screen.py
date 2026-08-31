import re

with open("app/src/main/java/com/example/ui/screens/auth/AuthScreen.kt", "r") as f:
    content = f.read()

# Add KeyboardOptions and KeyboardActions imports
imports = """import androidx.compose.foundation.text.KeyboardOptions
import androidx.compose.foundation.text.KeyboardActions
import androidx.compose.ui.text.input.ImeAction
"""
content = content.replace("import androidx.compose.ui.text.input.VisualTransformation", "import androidx.compose.ui.text.input.VisualTransformation\n" + imports)

# Modify password OutlinedTextField
password_field_old = """                    visualTransformation = if (passwordVisible) VisualTransformation.None else PasswordVisualTransformation(),
                    singleLine = true,"""
password_field_new = """                    visualTransformation = if (passwordVisible) VisualTransformation.None else PasswordVisualTransformation(),
                    singleLine = true,
                    keyboardOptions = KeyboardOptions(imeAction = ImeAction.Done),
                    keyboardActions = KeyboardActions(onDone = { 
                        keyboardController?.hide()
                        focusManager.clearFocus()
                        if (email.isNotBlank() && password.isNotBlank()) {
                            if (isSignUp) {
                                authViewModel.signUpWithEmail(email, password)
                            } else {
                                authViewModel.signInWithEmail(email, password)
                            }
                        }
                    }),"""
content = content.replace(password_field_old, password_field_new)

with open("app/src/main/java/com/example/ui/screens/auth/AuthScreen.kt", "w") as f:
    f.write(content)
