import re

filepath = 'app/src/main/java/com/example/navigation/AppNavigation.kt'
with open(filepath, 'r') as f:
    content = f.read()

# Add internet check
content = content.replace(
    'var isUpdatingData by remember { mutableStateOf(true) }',
    'var isUpdatingData by remember { mutableStateOf(com.example.utils.NetworkUtils.isInternetAvailable(context)) }'
)

with open(filepath, 'w') as f:
    f.write(content)

