import re

with open('app/src/main/java/com/example/navigation/AppNavigation.kt', 'r') as f:
    content = f.read()

# Add imports
if 'import com.example.utils.SiteVerificationManager' not in content:
    content = content.replace('import com.example.ui.components.BackgroundWebView', 'import com.example.ui.components.BackgroundWebView\nimport com.example.utils.SiteVerificationManager\nimport kotlinx.coroutines.delay')

# State variables
old_updating = 'var isUpdatingData by remember { mutableStateOf(true) }'
new_updating = """var isUpdatingData by remember { mutableStateOf(true) }
    var updateFinishedShowGreen by remember { mutableStateOf(false) }
    
    LaunchedEffect(updateFinishedShowGreen) {
        if (updateFinishedShowGreen) {
            delay(2000)
            isUpdatingData = false
            updateFinishedShowGreen = false
        }
    }
    
    val primaryColorVal = Color(if (primaryColor == 0) 0xFFE50914 else primaryColor.toLong())
"""
content = content.replace(old_updating, new_updating)

# BackgroundWebView usage
old_bg_webview = """        if (isUpdatingData && currentRoute != Screen.Splash.route && currentRoute != Screen.Auth.route && currentRoute != Screen.Onboarding.route) {
            BackgroundWebView(
                urls = extensionUrls,
                onProgress = { },
                onComplete = { isUpdatingData = false }
            )
        }"""
new_bg_webview = """        if (isUpdatingData && currentRoute != Screen.Splash.route && currentRoute != Screen.Auth.route && currentRoute != Screen.Onboarding.route && !updateFinishedShowGreen) {
            SiteVerificationManager.isVerificationStarted = true
            BackgroundWebView(
                urls = extensionUrls,
                onProgress = { },
                onSiteVerified = { url -> SiteVerificationManager.markSiteVerified(url) },
                onComplete = { 
                    SiteVerificationManager.isVerificationComplete = true
                    updateFinishedShowGreen = true 
                }
            )
        }"""
content = content.replace(old_bg_webview, new_bg_webview)

# Move the update box BELOW the topbar
# First, remove it from its current position
top_box_regex = r"                    if \(isUpdatingData && currentRoute != Screen\.Splash\.route && currentRoute != Screen\.Auth\.route && currentRoute != Screen\.Onboarding\.route\) \{[\s\S]*?\}\n                    \}\n"
# Actually, it's safer to just find and replace the whole Scaffold topBar block.
