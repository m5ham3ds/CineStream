import re

filepath = 'app/src/main/java/com/example/ui/screens/social/SocialScreen.kt'
with open(filepath, 'r') as f:
    content = f.read()

content = content.replace("import kotlinx.coroutines.launch", "import kotlinx.coroutines.launch\nimport kotlinx.coroutines.tasks.await")
content = content.replace("Divider(modifier = Modifier.padding(vertical = 16.dp))", "HorizontalDivider(modifier = Modifier.padding(vertical = 16.dp))")

with open(filepath, 'w') as f:
    f.write(content)
