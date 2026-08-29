import re

with open('app/src/main/java/com/example/ui/screens/player/TrailerScreen.kt', 'r') as f:
    content = f.read()

replacement = """@Composable
fun TrailerScreen(trailerId: String, onBack: () -> Unit) {
    Column(modifier = Modifier.fillMaxSize().background(Color.Black)) {
        Row(modifier = Modifier.fillMaxWidth().padding(16.dp)) {
            IconButton(onClick = onBack) {
                Icon(Icons.AutoMirrored.Filled.ArrowBack, contentDescription = "Back", tint = Color.White)
            }
        }
        
        if (trailerId.startsWith("local_offline_file://")) {
            Box(modifier = Modifier.fillMaxSize(), contentAlignment = androidx.compose.ui.Alignment.Center) {
                Column(horizontalAlignment = androidx.compose.ui.Alignment.CenterHorizontally) {
                    Icon(Icons.Default.DownloadDone, contentDescription = null, tint = Color.Green, modifier = Modifier.size(64.dp))
                    Spacer(modifier = Modifier.height(16.dp))
                    androidx.compose.material3.Text("يتم تشغيل الملف المحلي بدون إنترنت", color = Color.White, style = androidx.compose.material3.MaterialTheme.typography.titleLarge)
                    Spacer(modifier = Modifier.height(8.dp))
                    androidx.compose.material3.Text(trailerId.removePrefix("local_offline_file://"), color = Color.Gray)
                }
            }
        } else {
            AndroidView(
                modifier = Modifier.fillMaxSize(),
                factory = { context ->
                    val wasmDir = java.io.File(context.cacheDir, "WebView/Default/HTTP Cache/Code Cache/wasm")
                    if (!wasmDir.exists()) {
                        wasmDir.mkdirs()
                    }
                    
                    WebView(context).apply {
                        setLayerType(android.view.View.LAYER_TYPE_SOFTWARE, null)
                        settings.javaScriptEnabled = true
                        settings.domStorageEnabled = true
                        settings.mediaPlaybackRequiresUserGesture = false
                        webChromeClient = WebChromeClient()
                        webViewClient = WebViewClient()
                        val htmlData = \"\"\"
                            <html>
                                <body style="margin:0;padding:0;background-color:black;display:flex;justify-content:center;align-items:center;">
                                    <iframe width="100%" height="100%" src="https://www.youtube.com/embed/$trailerId?autoplay=1&fs=1&modestbranding=1&rel=0" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>
                                </body>
                            </html>
                        \"\"\".trimIndent()
                        loadData(htmlData, "text/html", "UTF-8")
                    }
                }
            )
        }
    }
}
"""

content = re.sub(r'@Composable\nfun TrailerScreen\(trailerId: String, onBack: \(\) -> Unit\) \{.*', replacement, content, flags=re.DOTALL)

# Also add import for DownloadDone if missing
if 'import androidx.compose.material.icons.filled.DownloadDone' not in content:
    content = content.replace('import androidx.compose.material.icons.Icons', 'import androidx.compose.material.icons.Icons\nimport androidx.compose.material.icons.filled.DownloadDone')

with open('app/src/main/java/com/example/ui/screens/player/TrailerScreen.kt', 'w') as f:
    f.write(content)

