import re

with open("app/src/main/java/com/example/ui/screens/profile/ProfileScreen.kt", "r") as f:
    content = f.read()

# Add necessary imports
imports = """import androidx.compose.material.icons.filled.Person
import androidx.compose.material.icons.outlined.Person
"""
content = content.replace("import androidx.compose.material.icons.outlined.*", "import androidx.compose.material.icons.outlined.*\n" + imports)

# We can also just use Icons.Default.Person everywhere since it exists.
content = content.replace("Icons.Outlined.Person", "Icons.Default.Person")
content = content.replace("Icons.Filled.Person", "Icons.Default.Person")

with open("app/src/main/java/com/example/ui/screens/profile/ProfileScreen.kt", "w") as f:
    f.write(content)
