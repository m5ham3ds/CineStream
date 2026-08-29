package com.example.ui.components

import android.annotation.SuppressLint
import android.os.Handler
import android.os.Looper
import android.webkit.CookieManager
import android.webkit.WebResourceRequest
import android.webkit.WebSettings
import android.webkit.WebView
import android.webkit.WebViewClient
import androidx.compose.foundation.layout.size
import androidx.compose.runtime.*
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.alpha
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.unit.dp
import androidx.compose.ui.viewinterop.AndroidView
import com.example.utils.NetworkUtils
import kotlinx.coroutines.delay

@SuppressLint("SetJavaScriptEnabled")
@Composable
fun BackgroundWebView(
    urls: List<String>,
    onProgress: (String) -> Unit,
    onSiteVerified: (String) -> Unit,
    onComplete: () -> Unit
) {
    val context = LocalContext.current
    var isInternetAvailable by remember { mutableStateOf(NetworkUtils.isInternetAvailable(context)) }
    
    if (!isInternetAvailable) {
        // Do not even start if no internet. Just wait or complete immediately.
        LaunchedEffect(Unit) {
            onComplete()
        }
        return
    }

    if (urls.isEmpty()) {
        LaunchedEffect(Unit) {
            onComplete()
        }
        return
    }

    var currentIndex by remember { mutableStateOf(0) }
    val currentUrl = if (currentIndex < urls.size) urls[currentIndex] else null
    
    // We will use a state to force reload if needed
    var reloadTrigger by remember { mutableStateOf(0) }

    if (currentUrl != null) {
        AndroidView(
            // Use 1.dp so it's technically rendered, but almost invisible
            modifier = Modifier.alpha(0.01f).size(1.dp), 
            factory = { ctx ->
                WebView(ctx).apply {
                    setLayerType(android.view.View.LAYER_TYPE_SOFTWARE, null)
                    settings.apply {
                        javaScriptEnabled = true
                        domStorageEnabled = true
                        userAgentString = "Mozilla/5.0 (Linux; Android 13; Pixel 7 Pro) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Mobile Safari/537.36"
                        mixedContentMode = WebSettings.MIXED_CONTENT_ALWAYS_ALLOW
                        cacheMode = WebSettings.LOAD_DEFAULT
                        mediaPlaybackRequiresUserGesture = false
                    }
                    
                    val cookieManager = CookieManager.getInstance()
                    cookieManager.setAcceptCookie(true)
                    cookieManager.setAcceptThirdPartyCookies(this, true)

                    webViewClient = object : WebViewClient() {
                        private var timeoutHandler = Handler(Looper.getMainLooper())
                        private var reloadRunnable: Runnable? = null

                        override fun onPageFinished(view: WebView, url: String) {
                            super.onPageFinished(view, url)
                            cookieManager.flush()
                            
                            // Cancel any previous reload timeout
                            reloadRunnable?.let { timeoutHandler.removeCallbacks(it) }
                            
                            // Evaluate the page content to see if we bypassed Cloudflare/Captcha
                            val jsCheck = """
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
                            """.trimIndent()
                            
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
                            }
                        }
                    }
                }
            },
            update = { webView ->
                // When url changes OR reload is triggered, we load/reload
                if (webView.url != currentUrl) {
                    onProgress(currentUrl)
                    webView.loadUrl(currentUrl)
                } else if (reloadTrigger > 0) {
                    webView.reload()
                }
            }
        )
    } else {
        LaunchedEffect(Unit) {
            onComplete()
        }
    }
}
