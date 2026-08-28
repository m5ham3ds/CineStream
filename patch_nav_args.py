import re

with open("app/src/main/java/com/example/navigation/AppNavigation.kt", "r") as f:
    content = f.read()

content = content.replace("onNavigateToNewReleases = { navController.navigate(Screen.NewReleases.route) }", "onNavigateToNewReleases = { navController.navigate(Screen.NewReleases.route) },\n                        onNavigateToUpcoming = { navController.navigate(Screen.Upcoming.route) }")

with open("app/src/main/java/com/example/navigation/AppNavigation.kt", "w") as f:
    f.write(content)

