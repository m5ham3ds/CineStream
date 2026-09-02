import re

with open("app/src/main/java/com/example/navigation/AppNavigation.kt", "r") as f:
    content = f.read()

bad_str = """            composable(Screen.PublicProfile.route) { backStackEntry ->
                val userId = backStackEntry.arguments?.getString("userId") ?: return@composable
                PublicProfileScreen(
                    userId = userId,
                    onBack = { navController.popBackStack() }
                )
            }
                )
            }"""
good_str = """            composable(Screen.PublicProfile.route) { backStackEntry ->
                val userId = backStackEntry.arguments?.getString("userId") ?: return@composable
                PublicProfileScreen(
                    userId = userId,
                    onBack = { navController.popBackStack() }
                )
            }"""

content = content.replace(bad_str, good_str)

with open("app/src/main/java/com/example/navigation/AppNavigation.kt", "w") as f:
    f.write(content)

