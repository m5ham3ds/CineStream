import re

with open("app/src/main/java/com/example/ui/screens/profile/ProfileScreen.kt", "r") as f:
    lines = f.readlines()

new_lines = []
coil_count = 0
for line in lines:
    if "import coil.compose.AsyncImage" in line:
        coil_count += 1
        if coil_count > 1:
            continue
    new_lines.append(line)

with open("app/src/main/java/com/example/ui/screens/profile/ProfileScreen.kt", "w") as f:
    f.writelines(new_lines)
