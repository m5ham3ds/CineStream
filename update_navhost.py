import re

filepath = 'app/src/main/java/com/example/navigation/AppNavigation.kt'
with open(filepath, 'r') as f:
    content = f.read()

# Add imports for the new screens
imports = """
import com.example.ui.screens.social.SocialScreen
import com.example.ui.screens.share.ShareScreen
"""
content = content.replace(
    'import com.example.ui.screens.settings.SettingsScreen',
    'import com.example.ui.screens.settings.SettingsScreen\n' + imports
)

# Add composables
nav_additions = """
            composable(Screen.Social.route) {
                SocialScreen(
                    onBack = { navController.popBackStack() }
                )
            }
            composable(Screen.Share.route) {
                ShareScreen(
                    onBack = { navController.popBackStack() }
                )
            }
"""

content = content.replace(
    'composable(Screen.Settings.route) {',
    nav_additions + '\n            composable(Screen.Settings.route) {'
)

with open(filepath, 'w') as f:
    f.write(content)

