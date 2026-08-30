import re

filepath = 'app/src/main/java/com/example/navigation/AppNavigation.kt'
with open(filepath, 'r') as f:
    content = f.read()

imports_to_add = """
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.verticalScroll
import androidx.compose.material.icons.outlined.Share
"""

content = content.replace("import androidx.compose.foundation.layout.*", "import androidx.compose.foundation.layout.*\n" + imports_to_add)

with open(filepath, 'w') as f:
    f.write(content)
