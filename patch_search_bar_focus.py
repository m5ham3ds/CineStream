import re

with open("app/src/main/java/com/example/ui/components/SearchBarDropdown.kt", "r") as f:
    content = f.read()

# Add FocusRequester and LaunchedEffect to request focus when expanded
if "import androidx.compose.ui.focus.FocusRequester" not in content:
    content = content.replace("import androidx.compose.ui.text.input.ImeAction", "import androidx.compose.ui.text.input.ImeAction\nimport androidx.compose.ui.focus.FocusRequester\nimport androidx.compose.ui.focus.focusRequester")

if "val focusRequester =" not in content:
    content = content.replace("val uiState by viewModel.uiState.collectAsState()", "val uiState by viewModel.uiState.collectAsState()\n    val focusRequester = remember { FocusRequester() }\n\n    LaunchedEffect(isExpanded) {\n        if (isExpanded) {\n            focusRequester.requestFocus()\n        }\n    }")
    
content = content.replace("modifier = Modifier.weight(1f),", "modifier = Modifier.weight(1f).focusRequester(focusRequester),")

with open("app/src/main/java/com/example/ui/components/SearchBarDropdown.kt", "w") as f:
    f.write(content)
