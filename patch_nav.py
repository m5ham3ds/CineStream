import re

with open("app/src/main/java/com/example/navigation/Screen.kt", "r") as f:
    content = f.read()

if "object Anime" not in content:
    content = content.replace("object Search : Screen(\"search\", \"Search\", Icons.Default.Search)", 
                              "object Search : Screen(\"search\", \"Search\", Icons.Default.Search)\n    object Anime : Screen(\"anime\", \"Anime\", Icons.Default.Tv)")

with open("app/src/main/java/com/example/navigation/Screen.kt", "w") as f:
    f.write(content)

with open("app/src/main/java/com/example/ui/components/BottomNavBar.kt", "r") as f:
    content = f.read()

new_items = """    val items = listOf(
        Screen.Home,
        Screen.Movies,
        Screen.Search,
        Screen.Series,
        Screen.Anime
    )"""

content = re.sub(r'val items = listOf\([^)]+\)', new_items, content, flags=re.MULTILINE)
content = content.replace("val label = if (screen == Screen.Library) \"المكتبات\" else screen.title", "val label = screen.title")

with open("app/src/main/java/com/example/ui/components/BottomNavBar.kt", "w") as f:
    f.write(content)
