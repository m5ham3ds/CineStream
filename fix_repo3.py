import re

filepath = 'app/src/main/java/com/example/data/repository/TmdbMediaRepositoryImpl.kt'
with open(filepath, 'r') as f:
    content = f.read()

# Replace `val thumb = parts.getOrNull(3)` with `val thumb = parts.getOrNull(3) ?: ""`
content = content.replace('val thumb = parts.getOrNull(3)', 'val thumb = parts.getOrNull(3) ?: ""')

with open(filepath, 'w') as f:
    f.write(content)
