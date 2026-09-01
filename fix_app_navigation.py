import re

with open("app/src/main/java/com/example/navigation/AppNavigation.kt", "r") as f:
    content = f.read()

profile_composable = """            composable(Screen.Profile.route) {
                ProfileScreen(
                    onNavigateToAuth = {
                        navController.navigate(Screen.Auth.route) { popUpTo(0) }
                    }
                )
            }"""

new_profile_composable = """            composable(Screen.Profile.route) {
                ProfileScreen(
                    onNavigateToAuth = {
                        navController.navigate(Screen.Auth.route) { popUpTo(0) }
                    },
                    onNavigateToEditProfile = {
                        navController.navigate(Screen.EditProfile.route)
                    }
                )
            }
            composable(Screen.EditProfile.route) {
                com.example.ui.screens.profile.EditProfileScreen(
                    onBack = { navController.popBackStack() }
                )
            }"""

if profile_composable in content:
    content = content.replace(profile_composable, new_profile_composable)
else:
    # try another format just in case
    profile_composable = """            composable(Screen.Profile.route) { 
                ProfileScreen(onNavigateToAuth = { 
                    navController.navigate(Screen.Auth.route) { popUpTo(0) }
                }) 
            }"""
    if profile_composable in content:
        content = content.replace(profile_composable, new_profile_composable)
    else:
        # manual replace
        content = re.sub(
            r'composable\(Screen\.Profile\.route\) \{[\s\S]*?\}\n',
            new_profile_composable + "\n",
            content
        )

with open("app/src/main/java/com/example/navigation/AppNavigation.kt", "w") as f:
    f.write(content)
