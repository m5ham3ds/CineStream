import re

with open("app/src/main/java/com/example/data/db/AppDatabase.kt", "r") as f:
    content = f.read()

content = content.replace("entities = [LibraryItem::class, DownloadItem::class]", "entities = [LibraryItem::class, DownloadItem::class, com.example.data.model.HistoryItem::class]")
content = content.replace("version = 1", "version = 2")
content = content.replace("abstract fun downloadDao(): DownloadDao", "abstract fun downloadDao(): DownloadDao\n    abstract fun historyDao(): HistoryDao")

with open("app/src/main/java/com/example/data/db/AppDatabase.kt", "w") as f:
    f.write(content)

