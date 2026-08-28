import re

with open("app/src/main/java/com/example/ui/ViewModelFactory.kt", "r") as f:
    content = f.read()

if "import com.example.ui.screens.anime.AnimeViewModel" not in content:
    content = content.replace("import com.example.ui.screens.home.HomeViewModel", "import com.example.ui.screens.home.HomeViewModel\nimport com.example.ui.screens.anime.AnimeViewModel")
    content = content.replace("            modelClass.isAssignableFrom(HomeViewModel::class.java) -> {", 
                              "            modelClass.isAssignableFrom(AnimeViewModel::class.java) -> {\n                AnimeViewModel(repository) as T\n            }\n            modelClass.isAssignableFrom(HomeViewModel::class.java) -> {")
    with open("app/src/main/java/com/example/ui/ViewModelFactory.kt", "w") as f:
        f.write(content)

with open("app/src/main/java/com/example/navigation/AppNavigation.kt", "r") as f:
    content = f.read()

# Add Anime to Drawer if it isn't there? Actually the request said add "Anime" to the bottom navigation bar. So it's already there in BottomNavBar.
# Let's add AnimeScreen composable to AppNavigation.kt
if "AnimeScreen(" not in content:
    content = content.replace("import com.example.ui.screens.home.HomeScreen", "import com.example.ui.screens.home.HomeScreen\nimport com.example.ui.screens.anime.AnimeScreen")
    
    # insert composable route
    anime_route = """        composable(Screen.Anime.route) {
            AnimeScreen(onAnimeClick = { seriesId ->
                navController.navigate(Screen.SeriesDetails.createRoute(seriesId))
            })
        }"""
    content = content.replace("composable(Screen.Series.route) {", anime_route + "\n        composable(Screen.Series.route) {")

    with open("app/src/main/java/com/example/navigation/AppNavigation.kt", "w") as f:
        f.write(content)

