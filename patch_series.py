import re

with open("app/src/main/java/com/example/ui/screens/series/SeriesScreen.kt", "r") as f:
    content = f.read()

# I will find the current block:
old_block = """        Spacer(modifier = Modifier.height(24.dp))

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

new_block = """        Spacer(modifier = Modifier.height(24.dp))

        if (selectedCategory == "Series") {
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
            }"""

if old_block in content:
    content = content.replace(old_block, new_block)
else:
    print("Old block not found in SeriesScreen.kt")

with open("app/src/main/java/com/example/ui/screens/series/SeriesScreen.kt", "w") as f:
    f.write(content)

