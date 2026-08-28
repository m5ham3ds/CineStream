import re

with open("app/src/main/java/com/example/navigation/Screen.kt", "r") as f:
    content = f.read()

content = content.replace("Screen(\"anime\", \"Anime\", Icons.Default.Tv)", "Screen(\"anime\", \"الأنمي\", Icons.Default.Tv)")

with open("app/src/main/java/com/example/navigation/Screen.kt", "w") as f:
    f.write(content)

with open("app/src/main/java/com/example/ui/components/BottomNavBar.kt", "r") as f:
    content = f.read()

# Let's ensure the label translation for other screens
# Movies = الأفلام, Series = المسلسلات, Search = البحث, Home = الرئيسية
trans = """                val label = when (screen) {
                    Screen.Home -> "الرئيسية"
                    Screen.Movies -> "الأفلام"
                    Screen.Series -> "المسلسلات"
                    Screen.Search -> "البحث"
                    Screen.Anime -> "الأنمي"
                    else -> screen.title
                }"""
content = re.sub(r'val label = .*', trans, content)

with open("app/src/main/java/com/example/ui/components/BottomNavBar.kt", "w") as f:
    f.write(content)
