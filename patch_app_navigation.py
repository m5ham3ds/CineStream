import re

with open("app/src/main/java/com/example/navigation/Screen.kt", "r") as f:
    content = f.read()

if "object Upcoming" not in content:
    content = content.replace("object NewReleases : Screen(\"new_releases\", \"New Releases\", Icons.Default.Movie)", "object NewReleases : Screen(\"new_releases\", \"New Releases\", Icons.Default.Movie)\n    object Upcoming : Screen(\"upcoming\", \"Coming Soon\", Icons.Default.Movie)")
    with open("app/src/main/java/com/example/navigation/Screen.kt", "w") as f:
        f.write(content)

with open("app/src/main/java/com/example/navigation/AppNavigation.kt", "r") as f:
    content = f.read()

imports = """
import com.example.ui.screens.home.UpcomingScreen
"""
if "import com.example.ui.screens.home.UpcomingScreen" not in content:
    content = content.replace("import com.example.ui.screens.home.NewReleasesScreen", "import com.example.ui.screens.home.NewReleasesScreen\nimport com.example.ui.screens.home.UpcomingScreen")

route = """
        composable(Screen.Upcoming.route) {
            UpcomingScreen(
                onItemClick = { id, isMovie ->
                    if (isMovie) {
                        navController.navigate(Screen.MovieDetails.createRoute(id))
                    } else {
                        navController.navigate(Screen.SeriesDetails.createRoute(id))
                    }
                },
                onBack = { navController.popBackStack() }
            )
        }
"""
if "composable(Screen.Upcoming.route)" not in content:
    content = content.replace("composable(Screen.NewReleases.route) {", route.strip() + "\n        composable(Screen.NewReleases.route) {")
    with open("app/src/main/java/com/example/navigation/AppNavigation.kt", "w") as f:
        f.write(content)
        
with open("app/src/main/java/com/example/ui/screens/home/HomeScreen.kt", "r") as f:
    content = f.read()

content = content.replace("onNavigateToNewReleases: () -> Unit = {}", "onNavigateToNewReleases: () -> Unit = {},\n    onNavigateToUpcoming: () -> Unit = {}")
content = content.replace("SectionTitle(\"Coming Soon\", onSeeAllClick = {})", "SectionTitle(\"Coming Soon\", onSeeAllClick = onNavigateToUpcoming)")
with open("app/src/main/java/com/example/ui/screens/home/HomeScreen.kt", "w") as f:
    f.write(content)

