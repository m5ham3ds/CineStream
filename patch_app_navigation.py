import re

with open("app/src/main/java/com/example/navigation/AppNavigation.kt", "r") as f:
    content = f.read()

# Add imports for new screens
imports = """import com.example.ui.screens.home.PopularScreen
import com.example.ui.screens.home.NewReleasesScreen
"""
content = content.replace("import com.example.ui.screens.home.TrendingScreen", imports + "import com.example.ui.screens.home.TrendingScreen")

# Replace MoviesScreen block
movies_old = """                composable(Screen.Movies.route) {
                    MoviesScreen(
                        onMovieClick = { id -> navController.navigate(Screen.MovieDetails.createRoute(id)) }
                    )
                }"""
movies_new = """                composable(Screen.Movies.route) {
                    MoviesScreen(
                        onMovieClick = { id -> navController.navigate(Screen.MovieDetails.createRoute(id)) },
                        onNavigateToTrending = { navController.navigate(Screen.Trending.route) },
                        onNavigateToWatching = { navController.navigate(Screen.Watching.route) },
                        onNavigateToPopular = { navController.navigate(Screen.Popular.route) },
                        onNavigateToNewReleases = { navController.navigate(Screen.NewReleases.route) }
                    )
                }"""
content = content.replace(movies_old, movies_new)

# Replace SeriesScreen block
series_old = """                composable(Screen.Series.route) {
                    SeriesScreen(
                        onSeriesClick = { id -> navController.navigate(Screen.SeriesDetails.createRoute(id)) }
                    )
                }"""
series_new = """                composable(Screen.Series.route) {
                    SeriesScreen(
                        onSeriesClick = { id -> navController.navigate(Screen.SeriesDetails.createRoute(id)) },
                        onNavigateToTrending = { navController.navigate(Screen.Trending.route) },
                        onNavigateToWatching = { navController.navigate(Screen.Watching.route) },
                        onNavigateToPopular = { navController.navigate(Screen.Popular.route) },
                        onNavigateToNewReleases = { navController.navigate(Screen.NewReleases.route) }
                    )
                }"""
content = content.replace(series_old, series_new)

# Replace SearchScreen block
search_old = """                composable(Screen.Search.route) {
                    SearchScreen(
                        onMediaClick = { id, isMovie ->
                            if (isMovie) {
                                navController.navigate(Screen.MovieDetails.createRoute(id))
                            } else {
                                navController.navigate(Screen.SeriesDetails.createRoute(id))
                            }
                        }
                    )
                }"""
search_new = """                composable(Screen.Search.route) {
                    SearchScreen(
                        onMediaClick = { id, isMovie ->
                            if (isMovie) {
                                navController.navigate(Screen.MovieDetails.createRoute(id))
                            } else {
                                navController.navigate(Screen.SeriesDetails.createRoute(id))
                            }
                        },
                        onNavigateToTrending = { navController.navigate(Screen.Trending.route) }
                    )
                }"""
content = content.replace(search_old, search_new)

# Add new routes near TrendingScreen
trending_str = """                composable(Screen.Trending.route) {
                    TrendingScreen(
                        onItemClick = { id, isMovie ->
                            if (isMovie) {
                                navController.navigate(Screen.MovieDetails.createRoute(id))
                            } else {
                                navController.navigate(Screen.SeriesDetails.createRoute(id))
                            }
                        },
                        onBack = { navController.popBackStack() }
                    )
                }"""

new_routes = """                composable(Screen.Popular.route) {
                    PopularScreen(
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
                composable(Screen.NewReleases.route) {
                    NewReleasesScreen(
                        onItemClick = { id, isMovie ->
                            if (isMovie) {
                                navController.navigate(Screen.MovieDetails.createRoute(id))
                            } else {
                                navController.navigate(Screen.SeriesDetails.createRoute(id))
                            }
                        },
                        onBack = { navController.popBackStack() }
                    )
                }"""
content = content.replace(trending_str, trending_str + "\n" + new_routes)

with open("app/src/main/java/com/example/navigation/AppNavigation.kt", "w") as f:
    f.write(content)

