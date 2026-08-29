import re

filepath = 'app/src/main/java/com/example/domain/providers/ProviderManager.kt'
with open(filepath, 'r') as f:
    content = f.read()

content = content.replace('val safeThumb = anime.thumbnailUrl?.replace("|", "")', 'val safeThumb = anime.thumbnailUrl?.replace("|", "") ?: ""')

with open(filepath, 'w') as f:
    f.write(content)
