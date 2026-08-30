import re

filepath = 'app/src/main/java/com/example/ui/components/BackgroundWebView.kt'
with open(filepath, 'r') as f:
    content = f.read()

content = content.replace("setLayerType(android.view.View.LAYER_TYPE_HARDWARE, null)", "setLayerType(android.view.View.LAYER_TYPE_SOFTWARE, null)")

with open(filepath, 'w') as f:
    f.write(content)
