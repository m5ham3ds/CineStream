import re

with open("app/src/main/java/com/example/MainActivity.kt", "r") as f:
    content = f.read()

# Add route for PersonDetails
if "composable(\"person/{personId}\")" not in content:
    person_route = """composable("person/{personId}") { backStackEntry ->
                        val personId = backStackEntry.arguments?.getString("personId") ?: ""
                        com.example.ui.screens.details.PersonDetailsScreen(
                            personId = personId,
                            onBack = { navController.navigateUp() },
                            onMovieClick = { navController.navigate("movie/$it") },
                            onSeriesClick = { navController.navigate("series/$it") }
                        )
                    }"""
    # Find the closing brace of NavHost
    content = content.replace("composable(\"downloads\")", person_route + "\n                    composable(\"downloads\")")

# Update navigations in MovieDetailsScreen and SeriesDetailsScreen usages in MainActivity
content = content.replace(
    """onBack = { navController.navigateUp() }
                        )""",
    """onBack = { navController.navigateUp() },
                            onPersonClick = { navController.navigate("person/$it") }
                        )"""
)

with open("app/src/main/java/com/example/MainActivity.kt", "w") as f:
    f.write(content)
