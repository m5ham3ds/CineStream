import re

with open("app/src/main/java/com/example/ui/screens/home/HomeScreen.kt", "r") as f:
    content = f.read()

categories_pattern = r"(        // Categories Tab Row.*?)(        // Hero Section.*?)(        Spacer\(modifier = Modifier.height\(24.dp\)\))"
match = re.search(categories_pattern, content, flags=re.DOTALL)
if match:
    categories = match.group(1)
    hero = match.group(2)
    spacer = match.group(3)
    new_order = hero + "\n        Spacer(modifier = Modifier.height(16.dp))\n" + categories + "\n" + spacer
    content = content.replace(match.group(0), new_order)

with open("app/src/main/java/com/example/ui/screens/home/HomeScreen.kt", "w") as f:
    f.write(content)
