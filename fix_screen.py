import re

with open("app/src/main/java/com/example/navigation/Screen.kt", "r") as f:
    content = f.read()

content = content.replace("object Profile : Screen(\"profile\", \"Profile\", Icons.Default.Person)", "object Profile : Screen(\"profile\", \"Profile\", Icons.Default.Person)\n    object EditProfile : Screen(\"edit_profile\", \"Edit Profile\", Icons.Default.Person)")

with open("app/src/main/java/com/example/navigation/Screen.kt", "w") as f:
    f.write(content)
