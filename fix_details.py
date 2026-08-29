import re

with open('app/src/main/java/com/example/ui/screens/details/DetailsScreens.kt', 'r') as f:
    content = f.read()

# Fix quality mismatch (source.quality -> source.quality.displayName)
content = content.replace("quality = source.quality", "quality = source.quality.displayName")

# Fix source.name -> source.serverName
content = content.replace("source.name", "source.serverName")

with open('app/src/main/java/com/example/ui/screens/details/DetailsScreens.kt', 'w') as f:
    f.write(content)

