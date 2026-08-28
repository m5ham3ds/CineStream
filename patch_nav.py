import re

with open("app/src/main/java/com/example/navigation/AppNavigation.kt", "r") as f:
    content = f.read()

# Add PersonDetails route
person_route = """
                composable("person/{personId}") { backStackEntry ->
                    val personId = backStackEntry.arguments?.getString("personId") ?: return@composable
                    com.example.ui.screens.details.PersonDetailsScreen(
                        personId = personId,
                        onBack = { navController.popBackStack() },
                        onMovieClick = { navController.navigate(Screen.MovieDetails.createRoute(it)) },
                        onSeriesClick = { navController.navigate(Screen.SeriesDetails.createRoute(it)) }
                    )
                }
"""

if "person/{personId}" not in content:
    content = content.replace("composable(Screen.MovieDetails.route) {", person_route + "\n                composable(Screen.MovieDetails.route) {")

content = content.replace(
    "MovieDetailsScreen(\n                        movieId = movieId, \n                        onBack = { navController.popBackStack() },\n                        onPlay = { url ->",
    "MovieDetailsScreen(\n                        movieId = movieId, \n                        onBack = { navController.popBackStack() },\n                        onPersonClick = { personId -> navController.navigate(\"person/$personId\") },\n                        onPlay = { url ->"
)

content = content.replace(
    "SeriesDetailsScreen(\n                        seriesId = seriesId, \n                        onBack = { navController.popBackStack() },\n                        onPlay = { url ->",
    "SeriesDetailsScreen(\n                        seriesId = seriesId, \n                        onBack = { navController.popBackStack() },\n                        onPersonClick = { personId -> navController.navigate(\"person/$personId\") },\n                        onPlay = { url ->"
)

with open("app/src/main/java/com/example/navigation/AppNavigation.kt", "w") as f:
    f.write(content)
