import re

with open('app/src/main/java/com/example/navigation/AppNavigation.kt', 'r') as f:
    content = f.read()

# Add imports
imports = """
import androidx.compose.ui.res.stringResource
import com.example.R
import com.example.ui.components.BackgroundWebView
"""
# We don't want to duplicate imports if they exist, but it's fine for python to just inject if needed.
if "com.example.ui.components.BackgroundWebView" not in content:
    content = content.replace('import androidx.compose.ui.text.font.FontWeight', 'import androidx.compose.ui.text.font.FontWeight\nimport com.example.ui.components.BackgroundWebView')

# Add state
states = """
    val bottomBarRoutes = listOf(Screen.Home.route, Screen.Movies.route, Screen.Series.route, Screen.Search.route, Screen.Anime.route)
    
    var isUpdatingData by remember { mutableStateOf(true) }
    val extensionUrls = remember { listOf("https://example.com/ext1", "https://example.com/ext2") }
"""
content = re.sub(r'val bottomBarRoutes = listOf\(.*?\)', states.strip(), content)

# Add TopBar banner
top_bar_banner = """
            topBar = {
                Column {
                    if (isUpdatingData && currentRoute != Screen.Splash.route && currentRoute != Screen.Auth.route && currentRoute != Screen.Onboarding.route) {
                        Box(
                            modifier = Modifier
                                .fillMaxWidth()
                                .background(Color(0xFF2C2C2E))
                                .padding(vertical = 4.dp),
                            contentAlignment = Alignment.Center
                        ) {
                            Text(
                                text = stringResource(R.string.updating_data),
                                color = Color.White,
                                fontSize = 12.sp
                            )
                        }
                    }
                    if (bottomBarRoutes.contains(currentRoute)
"""
content = re.sub(r'topBar = \{\s*if \(bottomBarRoutes\.contains\(currentRoute\)', top_bar_banner.strip(), content)

# Add BackgroundWebView at the end of the AppNavigation Composable
# Search for the final NavHost block end
background_webview = """
            ) {
"""

# Wait, it's safer to put it inside the Box/CompositionLocalProvider
# Let's put it right after Scaffold
scaffold_end_pattern = r'        }\s*\)\s*\{\s*innerPadding ->'
background_webview_insertion = """
        }
        
        if (isUpdatingData && currentRoute != Screen.Splash.route && currentRoute != Screen.Auth.route && currentRoute != Screen.Onboarding.route) {
            BackgroundWebView(
                urls = extensionUrls,
                onProgress = { },
                onComplete = { isUpdatingData = false }
            )
        }
        
        ) { innerPadding ->
"""

content = re.sub(scaffold_end_pattern, background_webview_insertion, content)

with open('app/src/main/java/com/example/navigation/AppNavigation.kt', 'w') as f:
    f.write(content)
