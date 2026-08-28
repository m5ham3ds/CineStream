import re

with open("app/src/main/java/com/example/ui/screens/details/DetailsScreens.kt", "r") as f:
    content = f.read()

content = content.replace("HistoryRepository(ctx) }            var showSourceSheet", "HistoryRepository(ctx) }\n            var showSourceSheet")

with open("app/src/main/java/com/example/ui/screens/details/DetailsScreens.kt", "w") as f:
    f.write(content)
