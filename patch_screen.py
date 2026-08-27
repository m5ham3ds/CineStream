import re

with open("app/src/main/java/com/example/navigation/Screen.kt", "r") as f:
    content = f.read()

content = content.replace(
    'object Watching : Screen("watching", "Continue Watching", Icons.Default.Tv)',
    'object Watching : Screen("watching", "Continue Watching", Icons.Default.Tv)\n    object Popular : Screen("popular", "Popular", Icons.Default.Movie)\n    object NewReleases : Screen("new_releases", "New Releases", Icons.Default.Movie)'
)

with open("app/src/main/java/com/example/navigation/Screen.kt", "w") as f:
    f.write(content)
