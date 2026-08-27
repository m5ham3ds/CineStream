import re

with open("app/src/main/java/com/example/navigation/AppNavigation.kt", "r") as f:
    content = f.read()

home_old = """                composable(Screen.Home.route) {
                    HomeScreen(
                        onMovieClick = { id -> navController.navigate(Screen.MovieDetails.createRoute(id)) },
                        onSeriesClick = { id -> navController.navigate(Screen.SeriesDetails.createRoute(id)) },
                        onNavigateToTrending = { navController.navigate(Screen.Trending.route) },
                        onNavigateToWatching = { navController.navigate(Screen.Watching.route) }
                    )
                }"""
home_new = """                composable(Screen.Home.route) {
                    HomeScreen(
                        onMovieClick = { id -> navController.navigate(Screen.MovieDetails.createRoute(id)) },
                        onSeriesClick = { id -> navController.navigate(Screen.SeriesDetails.createRoute(id)) },
                        onNavigateToTrending = { navController.navigate(Screen.Trending.route) },
                        onNavigateToWatching = { navController.navigate(Screen.Watching.route) },
                        onNavigateToPopular = { navController.navigate(Screen.Popular.route) },
                        onNavigateToNewReleases = { navController.navigate(Screen.NewReleases.route) }
                    )
                }"""
content = content.replace(home_old, home_new)

with open("app/src/main/java/com/example/navigation/AppNavigation.kt", "w") as f:
    f.write(content)
