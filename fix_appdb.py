import re

filepath = 'app/src/main/java/com/example/data/db/AppDatabase.kt'
with open(filepath, 'r') as f:
    content = f.read()

content = content.replace('import com.example.data.model.HistoryItem', 'import com.example.data.model.HistoryItem\nimport com.example.data.model.WatchedEpisode')
content = content.replace('entities = [LibraryItem::class, DownloadItem::class, HistoryItem::class]', 'entities = [LibraryItem::class, DownloadItem::class, HistoryItem::class, WatchedEpisode::class]')
content = content.replace('version = 2', 'version = 3')
content = content.replace('abstract fun historyDao(): HistoryDao', 'abstract fun historyDao(): HistoryDao\n    abstract fun watchedEpisodeDao(): WatchedEpisodeDao')

with open(filepath, 'w') as f:
    f.write(content)
