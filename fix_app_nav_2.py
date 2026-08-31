import re

with open("app/src/main/java/com/example/navigation/AppNavigation.kt", "r") as f:
    lines = f.readlines()

new_lines = []
content_scale_count = 0
for line in lines:
    if "import androidx.compose.ui.layout.ContentScale" in line:
        content_scale_count += 1
        if content_scale_count > 1:
            continue
    new_lines.append(line)

with open("app/src/main/java/com/example/navigation/AppNavigation.kt", "w") as f:
    f.writelines(new_lines)
