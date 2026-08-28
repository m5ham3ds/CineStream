import re

with open("app/src/main/java/com/example/navigation/AppNavigation.kt", "r") as f:
    content = f.read()

content = content.replace(
    "onNavigateToUpcoming = { navController.navigate(Screen.Upcoming.route) }",
    "onNavigateToUpcoming = { navController.navigate(Screen.Upcoming.route) },\n                        onNavigateToAnime = { navController.navigate(Screen.Anime.route) }"
)

with open("app/src/main/java/com/example/navigation/AppNavigation.kt", "w") as f:
    f.write(content)
