import re

with open("app/src/main/java/com/example/navigation/AppNavigation.kt", "r") as f:
    content = f.read()

imports_to_add = """import androidx.compose.runtime.setValue
"""
content = content.replace("import androidx.compose.runtime.getValue", "import androidx.compose.runtime.getValue\n" + imports_to_add)

with open("app/src/main/java/com/example/navigation/AppNavigation.kt", "w") as f:
    f.write(content)
