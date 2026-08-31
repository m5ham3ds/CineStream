import re

with open("app/src/main/java/com/example/ui/screens/auth/AuthScreen.kt", "r") as f:
    content = f.read()

# Add imports
import_target = """import androidx.compose.ui.platform.LocalContext"""
import_replacement = """import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.platform.LocalFocusManager
import androidx.compose.ui.platform.LocalSoftwareKeyboardController"""
content = content.replace(import_target, import_replacement)

# Add variables inside Composable
var_target = """    var showForgotPasswordDialog by remember { mutableStateOf(false) }"""
var_replacement = """    var showForgotPasswordDialog by remember { mutableStateOf(false) }
    val focusManager = LocalFocusManager.current
    val keyboardController = LocalSoftwareKeyboardController.current"""
content = content.replace(var_target, var_replacement)

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
