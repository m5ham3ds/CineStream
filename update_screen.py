import re

filepath = 'app/src/main/java/com/example/navigation/Screen.kt'
with open(filepath, 'r') as f:
    content = f.read()

if 'object Social' not in content:
    content = content.replace(
        'object SeriesDetails',
        'object Social : Screen("social", "Community", Icons.Default.Person)\n    object Share : Screen("share", "Offline Share", Icons.Default.Download)\n    object SeriesDetails'
    )
    with open(filepath, 'w') as f:
        f.write(content)

