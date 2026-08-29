import re

with open('app/src/main/java/com/example/MainActivity.kt', 'r') as f:
    content = f.read()

# Add LaunchedEffect import
if 'import androidx.compose.runtime.LaunchedEffect' not in content:
    content = content.replace('import androidx.compose.runtime.remember', 'import androidx.compose.runtime.remember\nimport androidx.compose.runtime.LaunchedEffect')

# Replace the locale logic
old_logic = """      // Update app language
      val currentLocales = AppCompatDelegate.getApplicationLocales()
      val desiredLanguage = if (appLanguage == "system") "" else appLanguage
      if (desiredLanguage.isNotEmpty() && currentLocales.toLanguageTags() != desiredLanguage) {
          AppCompatDelegate.setApplicationLocales(LocaleListCompat.forLanguageTags(desiredLanguage))
      } else if (desiredLanguage.isEmpty() && !currentLocales.isEmpty) {
          AppCompatDelegate.setApplicationLocales(LocaleListCompat.getEmptyLocaleList())
      }"""

new_logic = """      // Update app language
      LaunchedEffect(appLanguage) {
          val currentLocales = AppCompatDelegate.getApplicationLocales()
          val desiredLanguage = if (appLanguage == "system") "" else appLanguage
          if (desiredLanguage.isNotEmpty() && currentLocales.toLanguageTags() != desiredLanguage) {
              AppCompatDelegate.setApplicationLocales(LocaleListCompat.forLanguageTags(desiredLanguage))
          } else if (desiredLanguage.isEmpty() && !currentLocales.isEmpty) {
              AppCompatDelegate.setApplicationLocales(LocaleListCompat.getEmptyLocaleList())
          }
      }"""

content = content.replace(old_logic, new_logic)

with open('app/src/main/java/com/example/MainActivity.kt', 'w') as f:
    f.write(content)
