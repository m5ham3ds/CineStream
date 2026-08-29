import re

filepath = 'app/src/main/java/com/example/ui/screens/share/ShareScreen.kt'
with open(filepath, 'r') as f:
    content = f.read()

# Replace missing DownloadItem parameter
content = content.replace(
    'DownloadItem(id = id, title = title, posterUrl = "", progress = 1f, isMovie = isMovie, isCompleted = true, isPaused = false)',
    'DownloadItem(id = id, title = title, posterUrl = "", progress = 1f, isMovie = isMovie, isCompleted = true, isPaused = false, quality = "1080p")'
)

with open(filepath, 'w') as f:
    f.write(content)

