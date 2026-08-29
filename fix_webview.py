import re

filepath = 'app/src/main/java/com/example/ui/components/BackgroundWebView.kt'
with open(filepath, 'r') as f:
    content = f.read()

new_webview_init = """WebView(ctx).apply {
                    setLayerType(android.view.View.LAYER_TYPE_SOFTWARE, null)
                    settings.apply {"""

content = content.replace("WebView(ctx).apply {\n                    settings.apply {", new_webview_init)

with open(filepath, 'w') as f:
    f.write(content)
