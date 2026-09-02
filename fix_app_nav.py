import re

with open("app/src/main/java/com/example/navigation/AppNavigation.kt", "r") as f:
    content = f.read()

old_profile = """                ProfileScreen(
                    onNavigateToAuth = {
                        navController.navigate(Screen.Auth.route) { popUpTo(0) }
                    },
                    onNavigateToEditProfile = {
                        navController.navigate(Screen.EditProfile.route)
                    }
                )"""

new_profile = """                ProfileScreen(
                    onNavigateToAuth = {
                        navController.navigate(Screen.Auth.route) { popUpTo(0) }
                    },
                    onNavigateToEditProfile = {
                        navController.navigate(Screen.EditProfile.route)
                    },
                    onNavigateToSecurity = {
                        navController.navigate(Screen.Security.route)
                    },
                    onNavigateToSubscription = {
                        navController.navigate(Screen.Subscription.route)
                    },
                    onNavigateToSettings = {
                        navController.navigate(Screen.Settings.route)
                    }
                )"""

content = content.replace(old_profile, new_profile)

with open("app/src/main/java/com/example/navigation/AppNavigation.kt", "w") as f:
    f.write(content)
