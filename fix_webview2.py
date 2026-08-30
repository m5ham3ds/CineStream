import re

filepath = 'app/src/main/java/com/example/ui/components/BackgroundWebView.kt'
with open(filepath, 'r') as f:
    content = f.read()

# I will add a LaunchedEffect that automatically times out and forces next index
new_effect = """
    var currentIndex by remember { mutableStateOf(0) }
    val currentUrl = if (currentIndex < urls.size) urls[currentIndex] else null
    
    // Failsafe timeout: 5 seconds per URL
    LaunchedEffect(currentUrl) {
        if (currentUrl != null) {
            delay(5000)
            onSiteVerified(currentUrl)
            currentIndex++
        }
    }
"""

content = content.replace("var currentIndex by remember { mutableStateOf(0) }\n    val currentUrl = if (currentIndex < urls.size) urls[currentIndex] else null", new_effect)

with open(filepath, 'w') as f:
    f.write(content)
