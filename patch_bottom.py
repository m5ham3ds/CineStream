with open("app/src/main/java/com/example/ui/components/BottomNavBar.kt", "r") as f:
    content = f.read()

new_click = """                        .clickable {
                            if (selected) {
                                navController.popBackStack(screen.route, inclusive = true)
                                navController.navigate(screen.route)
                            } else {
                                navController.navigate(screen.route) {
                                    popUpTo(Screen.Home.route) {
                                        saveState = true
                                    }
                                    launchSingleTop = true
                                    restoreState = true
                                }
                            }
                        }"""

import re
content = re.sub(
    r'\.clickable \{.*?restoreState = true\n                            \}\n                        \}',
    new_click,
    content,
    flags=re.DOTALL
)

with open("app/src/main/java/com/example/ui/components/BottomNavBar.kt", "w") as f:
    f.write(content)
