import re

with open("app/src/main/java/com/example/ui/screens/auth/AuthScreen.kt", "r") as f:
    content = f.read()

# Add FocusManager and KeyboardController
import_target = """import androidx.compose.ui.platform.LocalContext"""
import_replacement = """import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.platform.LocalFocusManager
import androidx.compose.ui.platform.LocalSoftwareKeyboardController"""
content = content.replace(import_target, import_replacement)

focus_target = """    val context = LocalContext.current
    val scope = rememberCoroutineScope()
    val userPrefs = remember { com.example.data.local.UserPreferences(context) }"""
focus_replacement = """    val context = LocalContext.current
    val scope = rememberCoroutineScope()
    val userPrefs = remember { com.example.data.local.UserPreferences(context) }
    val focusManager = LocalFocusManager.current
    val keyboardController = LocalSoftwareKeyboardController.current"""
content = content.replace(focus_target, focus_replacement)

# Update onClick
click_target = """                    onClick = {
                        if (email.isNotBlank() && password.isNotBlank()) {"""
click_replacement = """                    onClick = {
                        focusManager.clearFocus()
                        keyboardController?.hide()
                        if (email.isNotBlank() && password.isNotBlank()) {"""
content = content.replace(click_target, click_replacement)

with open("app/src/main/java/com/example/ui/screens/auth/AuthScreen.kt", "w") as f:
    f.write(content)
