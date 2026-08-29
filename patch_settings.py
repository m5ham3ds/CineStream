import re

with open('app/src/main/java/com/example/ui/screens/settings/SettingsScreen.kt', 'r') as f:
    content = f.read()

# Add dialog states
dialog_states = """
    var showLanguageSheet by remember { mutableStateOf(false) }
    var showStartScreenSheet by remember { mutableStateOf(false) }
    
    var pendingThemeMode by remember { mutableStateOf<Int?>(null) }
    var pendingPrimaryColor by remember { mutableStateOf<Int?>(null) }
    var pendingLanguage by remember { mutableStateOf<String?>(null) }
"""
content = re.sub(r'var showLanguageSheet by remember { mutableStateOf\(false\) }.*var showStartScreenSheet by remember { mutableStateOf\(false\) }', dialog_states.strip(), content, flags=re.DOTALL)

# Replace theme changes
content = content.replace('coroutineScope.launch { userPrefs.saveThemeMode(0) }', 'pendingThemeMode = 0')
content = content.replace('coroutineScope.launch { userPrefs.saveThemeMode(1) }', 'pendingThemeMode = 1')
content = content.replace('coroutineScope.launch { userPrefs.saveThemeMode(2) }', 'pendingThemeMode = 2')

# Replace color changes
content = content.replace('coroutineScope.launch { userPrefs.savePrimaryColor(0) }', 'pendingPrimaryColor = 0')
content = content.replace('coroutineScope.launch { userPrefs.savePrimaryColor(1) }', 'pendingPrimaryColor = 1')
content = content.replace('coroutineScope.launch { userPrefs.savePrimaryColor(2) }', 'pendingPrimaryColor = 2')
content = content.replace('coroutineScope.launch { userPrefs.savePrimaryColor(3) }', 'pendingPrimaryColor = 3')
content = content.replace('coroutineScope.launch { userPrefs.savePrimaryColor(4) }', 'pendingPrimaryColor = 4')

# Replace language changes in bottom sheet
content = content.replace('coroutineScope.launch { userPrefs.saveAppLanguage("system"); showLanguageSheet = false }', '{ pendingLanguage = "system"; showLanguageSheet = false }')
content = content.replace('coroutineScope.launch { userPrefs.saveAppLanguage("en"); showLanguageSheet = false }', '{ pendingLanguage = "en"; showLanguageSheet = false }')
content = content.replace('coroutineScope.launch { userPrefs.saveAppLanguage("ar"); showLanguageSheet = false }', '{ pendingLanguage = "ar"; showLanguageSheet = false }')

# Add the dialogs before the end of the SettingsScreen function
dialogs = """
    // Confirmation Dialogs
    if (pendingThemeMode != null) {
        AlertDialog(
            onDismissRequest = { pendingThemeMode = null },
            title = { Text(stringResource(R.string.confirm_change)) },
            text = { Text(stringResource(R.string.confirm_theme_change)) },
            confirmButton = {
                TextButton(onClick = {
                    coroutineScope.launch { userPrefs.saveThemeMode(pendingThemeMode!!) }
                    pendingThemeMode = null
                }) { Text(stringResource(R.string.yes), color = MaterialTheme.colorScheme.primary) }
            },
            dismissButton = {
                TextButton(onClick = { pendingThemeMode = null }) { Text(stringResource(R.string.cancel), color = MaterialTheme.colorScheme.onSurface) }
            },
            containerColor = MaterialTheme.colorScheme.surface,
            titleContentColor = MaterialTheme.colorScheme.onSurface,
            textContentColor = MaterialTheme.colorScheme.onSurfaceVariant
        )
    }

    if (pendingPrimaryColor != null) {
        AlertDialog(
            onDismissRequest = { pendingPrimaryColor = null },
            title = { Text(stringResource(R.string.confirm_change)) },
            text = { Text(stringResource(R.string.confirm_color_change)) },
            confirmButton = {
                TextButton(onClick = {
                    coroutineScope.launch { userPrefs.savePrimaryColor(pendingPrimaryColor!!) }
                    pendingPrimaryColor = null
                }) { Text(stringResource(R.string.yes), color = MaterialTheme.colorScheme.primary) }
            },
            dismissButton = {
                TextButton(onClick = { pendingPrimaryColor = null }) { Text(stringResource(R.string.cancel), color = MaterialTheme.colorScheme.onSurface) }
            },
            containerColor = MaterialTheme.colorScheme.surface,
            titleContentColor = MaterialTheme.colorScheme.onSurface,
            textContentColor = MaterialTheme.colorScheme.onSurfaceVariant
        )
    }

    if (pendingLanguage != null) {
        AlertDialog(
            onDismissRequest = { pendingLanguage = null },
            title = { Text(stringResource(R.string.confirm_change)) },
            text = { Text(stringResource(R.string.confirm_language_change)) },
            confirmButton = {
                TextButton(onClick = {
                    coroutineScope.launch { userPrefs.saveAppLanguage(pendingLanguage!!) }
                    pendingLanguage = null
                }) { Text(stringResource(R.string.yes), color = MaterialTheme.colorScheme.primary) }
            },
            dismissButton = {
                TextButton(onClick = { pendingLanguage = null }) { Text(stringResource(R.string.cancel), color = MaterialTheme.colorScheme.onSurface) }
            },
            containerColor = MaterialTheme.colorScheme.surface,
            titleContentColor = MaterialTheme.colorScheme.onSurface,
            textContentColor = MaterialTheme.colorScheme.onSurfaceVariant
        )
    }
}
"""

content = content.replace('    // Start Screen Selection Sheet', dialogs + '\n    // Start Screen Selection Sheet')

with open('app/src/main/java/com/example/ui/screens/settings/SettingsScreen.kt', 'w') as f:
    f.write(content)
