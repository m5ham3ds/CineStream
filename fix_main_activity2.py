import re

with open('app/src/main/java/com/example/MainActivity.kt', 'r') as f:
    content = f.read()

content = content.replace(
    'val currentTag = if (currentLocales.isEmpty) "" else currentLocales[0]?.toLanguageTag() ?: ""',
    'val currentTag = if (currentLocales.isEmpty) "" else currentLocales.toLanguageTags()'
)

with open('app/src/main/java/com/example/MainActivity.kt', 'w') as f:
    f.write(content)
