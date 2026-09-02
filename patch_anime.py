import re

with open("app/src/main/java/com/example/ui/screens/anime/AnimeScreen.kt", "r") as f:
    content = f.read()

old_block = """        if (selectedCategory == animeStr) {
if (animeHistoryItems.isNotEmpty()) {"""

new_block = """        if (selectedCategory == animeStr) {
            if (animeHistoryItems.isNotEmpty()) {"""

content = content.replace(old_block, new_block)

with open("app/src/main/java/com/example/ui/screens/anime/AnimeScreen.kt", "w") as f:
    f.write(content)

