import re

with open("app/src/main/java/com/example/ui/screens/series/SeriesScreen.kt", "r") as f:
    content = f.read()

# I will find the duplicate block and remove it.
# The duplicate is right below if (selectedCategory == "Series") {
old_dup = """        if (selectedCategory == "Series") {if (seriesHistoryItems.isNotEmpty()) {
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

new_dup = """        if (selectedCategory == "Series") {"""

content = content.replace(old_dup, new_dup)

with open("app/src/main/java/com/example/ui/screens/series/SeriesScreen.kt", "w") as f:
    f.write(content)

