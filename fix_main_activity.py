import re

with open('app/src/main/java/com/example/MainActivity.kt', 'r') as f:
    content = f.read()

old_lang_block = """      val appLanguage by userPreferences.appLanguage.collectAsState(initial = "system")
      
      // Update app language
      LaunchedEffect(appLanguage) {
          val currentLocales = AppCompatDelegate.getApplicationLocales()
          val desiredLanguage = if (appLanguage == "system") "" else appLanguage
          if (desiredLanguage.isNotEmpty() && !currentLocales.toLanguageTags().contains(desiredLanguage)) {
              AppCompatDelegate.setApplicationLocales(LocaleListCompat.forLanguageTags(desiredLanguage))
          } else if (desiredLanguage.isEmpty() && !currentLocales.isEmpty) {
              AppCompatDelegate.setApplicationLocales(LocaleListCompat.getEmptyLocaleList())
          }
      }"""

new_lang_block = """      val appLanguage by userPreferences.appLanguage.collectAsState(initial = null)
      
      // Update app language
      LaunchedEffect(appLanguage) {
          if (appLanguage != null) {
              val currentLocales = AppCompatDelegate.getApplicationLocales()
              val desiredLanguage = if (appLanguage == "system") "" else appLanguage!!
              
              val currentTag = if (currentLocales.isEmpty) "" else currentLocales[0]?.toLanguageTag() ?: ""
              
              val needsUpdate = if (desiredLanguage.isEmpty()) {
                  !currentLocales.isEmpty
              } else {
                  !currentTag.startsWith(desiredLanguage)
              }
              
              if (needsUpdate) {
                  if (desiredLanguage.isEmpty()) {
                      AppCompatDelegate.setApplicationLocales(LocaleListCompat.getEmptyLocaleList())
                  } else {
                      AppCompatDelegate.setApplicationLocales(LocaleListCompat.forLanguageTags(desiredLanguage))
                  }
              }
          }
      }"""

content = content.replace(old_lang_block, new_lang_block)

with open('app/src/main/java/com/example/MainActivity.kt', 'w') as f:
    f.write(content)
