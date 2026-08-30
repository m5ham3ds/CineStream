import re

filepath = 'app/src/main/java/com/example/navigation/AppNavigation.kt'
with open(filepath, 'r') as f:
    content = f.read()

content = content.replace("import androidx.compose.foundation.rememberScrollState", "import androidx.compose.foundation.rememberScrollState\nimport androidx.compose.foundation.verticalScroll\nimport androidx.compose.material.icons.outlined.Share")

with open(filepath, 'w') as f:
    f.write(content)
