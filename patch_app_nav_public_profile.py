import re

with open("app/src/main/java/com/example/navigation/AppNavigation.kt", "r") as f:
    content = f.read()

import_stmt = "import com.example.ui.screens.profile.PublicProfileScreen"
if import_stmt not in content:
    content = content.replace("import com.example.ui.screens.profile.ProfileScreen", "import com.example.ui.screens.profile.ProfileScreen\nimport com.example.ui.screens.profile.PublicProfileScreen")

route_code = """            composable(Screen.EditProfile.route) {
                com.example.ui.screens.profile.EditProfileScreen(
                    onBack = { navController.popBackStack() }
                )
            }
            
            composable(Screen.PublicProfile.route) { backStackEntry ->
                val userId = backStackEntry.arguments?.getString("userId") ?: return@composable
                PublicProfileScreen(
                    userId = userId,
                    onBack = { navController.popBackStack() }
                )
            }"""

content = re.sub(r"            composable\(Screen\.EditProfile\.route\) \{(.*?)\}", route_code, content, flags=re.DOTALL)

with open("app/src/main/java/com/example/navigation/AppNavigation.kt", "w") as f:
    f.write(content)

