import re

filepath = 'app/src/main/java/com/example/ui/screens/social/SocialScreen.kt'
with open(filepath, 'r') as f:
    content = f.read()

content = content.replace("Modifier.padding(horizontal = 16.dp, bottom = 8.dp)", "Modifier.padding(horizontal = 16.dp).padding(bottom = 8.dp)")

with open(filepath, 'w') as f:
    f.write(content)
