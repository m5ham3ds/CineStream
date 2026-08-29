import re
import os

filepath = 'app/src/main/java/com/example/ui/components/CustomTopBar.kt'
with open(filepath, 'r') as f:
    content = f.read()

# Add statusBarsPadding() back
content = content.replace(
    '// Removed statusBarsPadding() because it\'s handled by Scaffold padding',
    '.statusBarsPadding()'
)

with open(filepath, 'w') as f:
    f.write(content)

