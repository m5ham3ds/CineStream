import re

# Fix ShareScreen.kt
filepath = 'app/src/main/java/com/example/ui/screens/share/ShareScreen.kt'
with open(filepath, 'r') as f:
    content = f.read()

content = content.replace("Build.VERSION_CODES.S", "android.os.Build.VERSION_CODES.S")
content = content.replace("Build.VERSION.CODES.S", "android.os.Build.VERSION_CODES.S")

with open(filepath, 'w') as f:
    f.write(content)

# Fix P2PManager.kt
filepath = 'app/src/main/java/com/example/utils/P2PManager.kt'
with open(filepath, 'r') as f:
    content = f.read()

old_invoke = "onMovieReceived?.invoke(id, title, isMovie)"
new_invoke = """val posterUrl = incomingMetadata!!.optString("posterUrl", "")
                    onMovieReceived?.invoke(id, title, isMovie, posterUrl)"""

content = content.replace(old_invoke, new_invoke)

with open(filepath, 'w') as f:
    f.write(content)
