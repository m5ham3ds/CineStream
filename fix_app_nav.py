import re

with open("app/src/main/java/com/example/navigation/AppNavigation.kt", "r") as f:
    content = f.read()

# Fix double import of ContentScale
content = content.replace("import androidx.compose.ui.layout.ContentScale\nimport androidx.compose.ui.layout.ContentScale", "import androidx.compose.ui.layout.ContentScale")
content = content.replace("import androidx.compose.ui.layout.ContentScale\n\nimport androidx.compose.ui.layout.ContentScale", "import androidx.compose.ui.layout.ContentScale")

with open("app/src/main/java/com/example/navigation/AppNavigation.kt", "w") as f:
    f.write(content)
