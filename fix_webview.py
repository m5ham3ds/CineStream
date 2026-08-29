import re

with open('app/src/main/java/com/example/ui/components/BackgroundWebView.kt', 'r') as f:
    content = f.read()

content = content.replace(
    'onProgress: (String) -> Unit,',
    'onProgress: (String) -> Unit,\n    onSiteVerified: (String) -> Unit,'
)

old_launched_effect = """    LaunchedEffect(currentUrl) {
        if (currentUrl != null) {
            onProgress(currentUrl)
            // Wait 8 seconds for the WebView to process Cloudflare/Captcha
            delay(8000)
            currentIndex++
        } else {
            onComplete()
        }
    }"""

new_launched_effect = """    LaunchedEffect(currentUrl) {
        if (currentUrl != null) {
            onProgress(currentUrl)
            // Wait 8 seconds for the WebView to process Cloudflare/Captcha
            delay(8000)
            onSiteVerified(currentUrl)
            currentIndex++
        } else {
            onComplete()
        }
    }"""

content = content.replace(old_launched_effect, new_launched_effect)

with open('app/src/main/java/com/example/ui/components/BackgroundWebView.kt', 'w') as f:
    f.write(content)
