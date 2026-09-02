import re

with open("app/src/main/java/com/example/ui/screens/series/SeriesScreen.kt", "r") as f:
    content = f.read()

# Remove the Continue Watching inside the if check, and just leave if (selectedCategory == "Series") {
content = re.sub(
    r'if \(selectedCategory == "Series"\) \{if \(seriesHistoryItems\.isNotEmpty\(\)\) \{.*?Spacer\(modifier = Modifier\.height\(24\.dp\)\)\s*\}',
    r'if (selectedCategory == "Series") {',
    content,
    flags=re.DOTALL
)

# Add Continue Watching below Categories Tab Row
categories_block_end = r'\}\s*Spacer\(modifier = Modifier\.height\(24\.dp\)\)\s*if \(selectedCategory == "Series"\) \{'

new_block = """}
        Spacer(modifier = Modifier.height(24.dp))

        if (seriesHistoryItems.isNotEmpty()) {
            SectionTitleShared(stringResource(R.string.continue_watching), onSeeAllClick = onNavigateToWatching)
            LazyRow(
                contentPadding = PaddingValues(horizontal = 16.dp),
                horizontalArrangement = Arrangement.spacedBy(16.dp)
            ) {
                items(seriesHistoryItems) { item ->
                    ContinueWatchingCardShared(item = item) {
                        onSeriesClick(item.id)
                    }
                }
            }
            Spacer(modifier = Modifier.height(24.dp))
        }

        if (selectedCategory == "Series") {"""

content = re.sub(categories_block_end, new_block, content, flags=re.DOTALL)

with open("app/src/main/java/com/example/ui/screens/series/SeriesScreen.kt", "w") as f:
    f.write(content)

