with open("app/src/main/java/com/example/navigation/AppNavigation.kt", "r") as f:
    content = f.read()

trailer_route = """
                composable("trailer/{trailerId}") { backStackEntry ->
                    val trailerId = backStackEntry.arguments?.getString("trailerId") ?: return@composable
                    com.example.ui.screens.player.TrailerScreen(trailerId = trailerId, onBack = { navController.popBackStack() })
                }
"""

if "trailer/{trailerId}" not in content:
    content = content.replace("composable(\"player?url={url}\") {", trailer_route + "\n                composable(\"player?url={url}\") {")
    with open("app/src/main/java/com/example/navigation/AppNavigation.kt", "w") as f:
        f.write(content)
