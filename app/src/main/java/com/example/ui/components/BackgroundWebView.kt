package com.example.ui.components

import android.annotation.SuppressLint
import android.webkit.CookieManager
import android.webkit.WebSettings
import android.webkit.WebView
import android.webkit.WebViewClient
import androidx.compose.foundation.layout.size
import androidx.compose.runtime.*
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.alpha
import androidx.compose.ui.unit.dp
import androidx.compose.ui.viewinterop.AndroidView
import kotlinx.coroutines.delay

@SuppressLint("SetJavaScriptEnabled")
@Composable
fun BackgroundWebView(
    urls: List<String>,
    onProgress: (String) -> Unit,
    onComplete: () -> Unit
) {
    if (urls.isEmpty()) {
        LaunchedEffect(Unit) {
            onComplete()
        }
        return
    }

    var currentIndex by remember { mutableStateOf(0) }
    val currentUrl = if (currentIndex < urls.size) urls[currentIndex] else null

    LaunchedEffect(currentUrl) {
        if (currentUrl != null) {
            onProgress(currentUrl)
            // Wait 8 seconds for the WebView to process Cloudflare/Captcha
            delay(8000)
            currentIndex++
        } else {
            onComplete()
        }
    }

    if (currentUrl != null) {
        AndroidView(
            modifier = Modifier.alpha(0f).size(1.dp), // Invisible
            factory = { context ->
                WebView(context).apply {
                    settings.apply {
                        javaScriptEnabled = true
                        domStorageEnabled = true
                        // Use a modern desktop or mobile user agent
                        userAgentString = "Mozilla/5.0 (Linux; Android 13; Pixel 7 Pro) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Mobile Safari/537.36"
                        mixedContentMode = WebSettings.MIXED_CONTENT_ALWAYS_ALLOW
                        cacheMode = WebSettings.LOAD_DEFAULT
                    }
                    
                    val cookieManager = CookieManager.getInstance()
                    cookieManager.setAcceptCookie(true)
                    cookieManager.setAcceptThirdPartyCookies(this, true)

                    webViewClient = object : WebViewClient() {
                        override fun onPageFinished(view: WebView?, url: String?) {
                            super.onPageFinished(view, url)
                            // Let the cookie manager flush in case of new cookies
                            CookieManager.getInstance().flush()
                        }
                    }
                }
            },
            update = { webView ->
                if (webView.url != currentUrl && currentUrl != null) {
                    webView.loadUrl(currentUrl)
                }
            }
        )
    }
}
