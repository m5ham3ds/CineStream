import re

with open("app/src/main/java/com/example/ui/screens/series/SeriesScreen.kt", "r") as f:
    content = f.read()

# Replace the inner block using regex
content = re.sub(
    r'if \(selectedCategory == "Series"\) \{if \(seriesHistoryItems\.isNotEmpty\(\)\) \{.*?Spacer\(modifier = Modifier\.height\(24\.dp\)\)\s*\}',
    r'if (selectedCategory == "Series") {',
    content,
    flags=re.DOTALL
)

with open("app/src/main/java/com/example/ui/screens/series/SeriesScreen.kt", "w") as f:
    f.write(content)

