import re

with open("app/src/main/java/com/example/navigation/AppNavigation.kt", "r") as f:
    content = f.read()

content = content.replace(
    "val bottomBarRoutes = listOf(\n        Screen.Home.route,\n        Screen.Movies.route,\n        Screen.Series.route,\n        Screen.Search.route,\n        Screen.Library.route\n    )",
    "val bottomBarRoutes = listOf(\n        Screen.Home.route,\n        Screen.Movies.route,\n        Screen.Series.route,\n        Screen.Search.route,\n        Screen.Library.route,\n        Screen.Anime.route\n    )"
)

with open("app/src/main/java/com/example/navigation/AppNavigation.kt", "w") as f:
    f.write(content)
