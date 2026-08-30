import re

filepath = 'app/src/main/java/com/example/data/repository/DownloadRepository.kt'
with open(filepath, 'r') as f:
    content = f.read()

new_fun = """    suspend fun addCompletedDownload(item: DownloadItem) {
        downloadDao.insertItem(item)
    }
"""

content = content.replace("suspend fun addToDownloads(item: DownloadItem) {", new_fun + "\n    suspend fun addToDownloads(item: DownloadItem) {")

with open(filepath, 'w') as f:
    f.write(content)
