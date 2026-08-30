import re

filepath = 'app/src/main/java/com/example/ui/components/BackgroundWebView.kt'
with open(filepath, 'r') as f:
    content = f.read()

# 1. Remove the bad LaunchedEffect failsafe timeout
bad_effect_pattern = r"\s*// Failsafe timeout: 5 seconds per URL\s*LaunchedEffect\(currentUrl\) \{\s*if \(currentUrl != null\) \{\s*delay\(5000\)\s*onSiteVerified\(currentUrl\)\s*currentIndex\+\+\s*\}\s*\}"
content = re.sub(bad_effect_pattern, "", content)

# 2. Fix Modifier for AndroidView
# From: modifier = Modifier.alpha(0.01f).size(1.dp),
# To: modifier = Modifier.fillMaxSize().alpha(0.02f),
content = content.replace("modifier = Modifier.alpha(0.01f).size(1.dp),", "modifier = androidx.compose.foundation.layout.fillMaxSize().alpha(0.02f),")

# 3. Update WebView Settings (hardware acceleration, user agent)
old_settings = """                    setLayerType(android.view.View.LAYER_TYPE_SOFTWARE, null)
                    settings.apply {
                        javaScriptEnabled = true
                        domStorageEnabled = true
                        userAgentString = "Mozilla/5.0 (Linux; Android 13; Pixel 7 Pro) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Mobile Safari/537.36"
                        mixedContentMode = WebSettings.MIXED_CONTENT_ALWAYS_ALLOW
                        cacheMode = WebSettings.LOAD_DEFAULT
                        mediaPlaybackRequiresUserGesture = false
                    }"""

new_settings = """                    setLayerType(android.view.View.LAYER_TYPE_HARDWARE, null)
                    settings.apply {
                        javaScriptEnabled = true
                        domStorageEnabled = true
                        databaseEnabled = true
                        javaScriptCanOpenWindowsAutomatically = true
                        userAgentString = WebSettings.getDefaultUserAgent(ctx)
                        mixedContentMode = WebSettings.MIXED_CONTENT_ALWAYS_ALLOW
                        cacheMode = WebSettings.LOAD_DEFAULT
                        mediaPlaybackRequiresUserGesture = false
                    }"""
content = content.replace(old_settings, new_settings)

# 4. Enhance JS checking
old_js = """                            val jsCheck = \"\"\"
                                (function() {
                                    var title = document.title.toLowerCase();
                                    var body = document.body.innerText.toLowerCase();
                                    var hasCloudflare = title.includes('just a moment') ||
                                                         body.includes('cloudflare') ||
                                                         body.includes('security check') ||
                                                         body.includes('تأكد من أنك لست روبوت') ||
                                                         body.includes('robot');
                                    
                                    if (hasCloudflare) {
                                        // Attempt to find and click checkboxes or turnstile wrappers
                                        var cf = document.querySelector('.cf-turnstile-wrapper, #challenge-stage, input[type="checkbox"]');
                                        if (cf) { cf.click(); }
                                        return 'CAPTCHA';
                                    } else if (body.length > 50) {
                                        return 'SUCCESS';
                                    }
                                    return 'UNKNOWN';
                                })();
                            \"\"\".trimIndent()
                            
                            view.evaluateJavascript(jsCheck) { result ->
                                val res = result?.replace("\"", "") ?: "UNKNOWN"
                                if (res == "SUCCESS") {
                                    // Successfully bypassed
                                    onSiteVerified(currentUrl)
                                    currentIndex++
                                } else {
                                    // It's a captcha or unknown. Schedule a reload after 10 seconds if it doesn't navigate away.
                                    reloadRunnable = Runnable {
                                        reloadTrigger++
                                    }
                                    timeoutHandler.postDelayed(reloadRunnable!!, 10000)
                                }
                            }"""

new_js = """                            val jsCheck = \"\"\"
                                (function() {
                                    // Continuously try to click Cloudflare/captcha elements every 1 second
                                    setInterval(function() {
                                        var cf = document.querySelector('.cf-turnstile-wrapper, #challenge-stage, input[type="checkbox"], #challenge-form');
                                        if (cf) { cf.click(); }
                                        // Sometimes it's inside an iframe
                                        var iframes = document.querySelectorAll('iframe');
                                        for (var i = 0; i < iframes.length; i++) {
                                            try {
                                                var innerBtn = iframes[i].contentWindow.document.querySelector('input[type="checkbox"]');
                                                if (innerBtn) innerBtn.click();
                                            } catch(e) {}
                                        }
                                    }, 1000);
                                    
                                    var title = document.title.toLowerCase();
                                    var body = document.body.innerText.toLowerCase();
                                    var hasCloudflare = title.includes('just a moment') || 
                                                        title.includes('attention required') ||
                                                         body.includes('cloudflare') ||
                                                         body.includes('security check') ||
                                                         body.includes('تأكد من أنك لست روبوت') ||
                                                         body.includes('robot');
                                    
                                    if (hasCloudflare) {
                                        return 'CAPTCHA';
                                    } else if (body.length > 50) {
                                        return 'SUCCESS';
                                    }
                                    return 'UNKNOWN';
                                })();
                            \"\"\".trimIndent()
                            
                            // We need to continuously check because page content can change dynamically without onPageFinished
                            val checkRunnable = object : Runnable {
                                override fun run() {
                                    view.evaluateJavascript(jsCheck) { result ->
                                        val res = result?.replace("\"", "") ?: "UNKNOWN"
                                        if (res == "SUCCESS") {
                                            cookieManager.flush()
                                            onSiteVerified(currentUrl)
                                            currentIndex++
                                        } else {
                                            // Keep checking
                                            timeoutHandler.postDelayed(this, 2000)
                                        }
                                    }
                                }
                            }
                            timeoutHandler.postDelayed(checkRunnable, 1000)"""

content = content.replace(old_js, new_js)

with open(filepath, 'w') as f:
    f.write(content)
