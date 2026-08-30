import re

filepath = 'app/src/main/java/com/example/ui/screens/share/ShareScreen.kt'
with open(filepath, 'r') as f:
    content = f.read()

content = content.replace("downloadRepository.addToDownloads(", "downloadRepository.addCompletedDownload(")

with open(filepath, 'w') as f:
    f.write(content)
