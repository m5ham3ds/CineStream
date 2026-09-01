import re

with open("app/src/main/java/com/example/navigation/AppNavigation.kt", "r") as f:
    content = f.read()

# Fix ProfileScreen navigation
content = content.replace("ProfileScreen()", "ProfileScreen(onNavigateToAuth = {\n                        scope.launch { \n                            userPrefs.saveIsLoggedIn(false)\n                            userPrefs.saveIsGuest(true)\n                        }\n                        navController.navigate(Screen.Auth.route) { popUpTo(0) }\n                    })")

# Fix Sidebar logout logic
sidebar_logout_old = """                        scope.launch { userPrefs.saveIsGuest(true) }
                        navController.navigate(Screen.Auth.route) { popUpTo(0) }"""
sidebar_logout_new = """                        scope.launch { 
                            userPrefs.saveIsGuest(true)
                            userPrefs.saveIsLoggedIn(false)
                        }
                        authViewModel.signOut()
                        navController.navigate(Screen.Auth.route) { popUpTo(0) }"""
content = content.replace(sidebar_logout_old, sidebar_logout_new)

with open("app/src/main/java/com/example/navigation/AppNavigation.kt", "w") as f:
    f.write(content)
