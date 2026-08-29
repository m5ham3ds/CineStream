import re

filepath = 'app/src/main/java/com/example/ui/screens/share/ShareScreen.kt'
with open(filepath, 'r') as f:
    content = f.read()

# Replace the problematic line
old_line = "val completedDownloads by downloadRepository.getAllCompletedDownloads().collectAsState(initial = emptyList())"
new_line = """
    val allDownloads by downloadRepository.getDownloadItems().collectAsState(initial = emptyList())
    val completedDownloads = remember(allDownloads) { allDownloads.filter { it.isCompleted } }
"""
content = content.replace(old_line, new_line)

with open(filepath, 'w') as f:
    f.write(content)
