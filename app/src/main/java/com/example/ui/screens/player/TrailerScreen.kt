package com.example.ui.screens.player

import android.webkit.WebChromeClient
import android.webkit.WebView
import android.webkit.WebViewClient
import androidx.compose.foundation.background
import androidx.compose.foundation.layout.*
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.automirrored.filled.ArrowBack
import androidx.compose.material3.Icon
import androidx.compose.material3.IconButton
import androidx.compose.runtime.Composable
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.unit.dp
import androidx.compose.ui.viewinterop.AndroidView

@Composable
fun TrailerScreen(trailerId: String, onBack: () -> Unit) {
    Column(modifier = Modifier.fillMaxSize().background(Color.Black)) {
        Row(modifier = Modifier.fillMaxWidth().padding(16.dp)) {
            IconButton(onClick = onBack) {
                Icon(Icons.AutoMirrored.Filled.ArrowBack, contentDescription = "Back", tint = Color.White)
            }
        }
        AndroidView(
            modifier = Modifier.fillMaxSize(),
            factory = { context ->
                WebView(context).apply {
                    settings.javaScriptEnabled = true
                    settings.domStorageEnabled = true
                    settings.mediaPlaybackRequiresUserGesture = false
                    webChromeClient = WebChromeClient()
                    webViewClient = WebViewClient()
                    val htmlData = """
                        <html>
                            <body style="margin:0;padding:0;background-color:black;display:flex;justify-content:center;align-items:center;">
                                <iframe width="100%" height="100%" src="https://www.youtube.com/embed/$trailerId?autoplay=1&fs=1&modestbranding=1&rel=0" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>
                            </body>
                        </html>
                    """.trimIndent()
                    loadData(htmlData, "text/html", "UTF-8")
                }
            }
        )
    }
}
