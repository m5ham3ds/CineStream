import re

with open('app/src/main/java/com/example/ui/screens/settings/SettingsScreen.kt', 'r') as f:
    content = f.read()

# For pendingThemeMode
old_theme = """                TextButton(onClick = {
                    coroutineScope.launch { userPrefs.saveThemeMode(pendingThemeMode!!) }
                    pendingThemeMode = null
                })"""
new_theme = """                TextButton(onClick = {
                    val mode = pendingThemeMode
                    if (mode != null) {
                        coroutineScope.launch { userPrefs.saveThemeMode(mode) }
                    }
                    pendingThemeMode = null
                })"""
content = content.replace(old_theme, new_theme)

# For pendingPrimaryColor
old_color = """                TextButton(onClick = {
                    coroutineScope.launch { userPrefs.savePrimaryColor(pendingPrimaryColor!!) }
                    pendingPrimaryColor = null
                })"""
new_color = """                TextButton(onClick = {
                    val color = pendingPrimaryColor
                    if (color != null) {
                        coroutineScope.launch { userPrefs.savePrimaryColor(color) }
                    }
                    pendingPrimaryColor = null
                })"""
content = content.replace(old_color, new_color)

# For pendingLanguage
old_lang = """                TextButton(onClick = {
                    coroutineScope.launch { userPrefs.saveAppLanguage(pendingLanguage!!) }
                    pendingLanguage = null
                })"""
new_lang = """                TextButton(onClick = {
                    val lang = pendingLanguage
                    if (lang != null) {
                        coroutineScope.launch { userPrefs.saveAppLanguage(lang) }
                    }
                    pendingLanguage = null
                })"""
content = content.replace(old_lang, new_lang)

with open('app/src/main/java/com/example/ui/screens/settings/SettingsScreen.kt', 'w') as f:
    f.write(content)
