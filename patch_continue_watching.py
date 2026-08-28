import re

history_state = """
    val historyItems by historyRepository.getHistoryItems().collectAsState(initial = emptyList())
    val movieHistoryItems = historyItems.filter { it.isMovie }
"""

history_state_series = """
    val historyItems by historyRepository.getHistoryItems().collectAsState(initial = emptyList())
    val seriesHistoryItems = historyItems.filter { !it.isMovie }
"""

history_ui_movies = """
        if (movieHistoryItems.isNotEmpty()) {
            SectionTitleShared("متابعة المشاهدة", onSeeAllClick = onNavigateToWatching)
            LazyRow(
                contentPadding = PaddingValues(horizontal = 16.dp),
                horizontalArrangement = Arrangement.spacedBy(16.dp)
            ) {
                items(movieHistoryItems) { item ->
                    ContinueWatchingCardShared(item = item) {
                        onMovieClick(item.id)
                    }
                }
            }
            Spacer(modifier = Modifier.height(24.dp))
        }
"""

history_ui_series = """
        if (seriesHistoryItems.isNotEmpty()) {
            SectionTitleShared("متابعة المشاهدة", onSeeAllClick = onNavigateToWatching)
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
"""

# MoviesScreen
with open("app/src/main/java/com/example/ui/screens/movies/MoviesScreen.kt", "r") as f:
    content = f.read()

if "historyItems" not in content:
    content = content.replace("val downloadRepository = remember { DownloadRepository(context) }", "val historyRepository = remember { com.example.data.repository.HistoryRepository(context) }\n    val downloadRepository = remember { DownloadRepository(context) }\n" + history_state)

content = re.sub(r'SectionTitleShared\("Continue Watching", onSeeAllClick = onNavigateToWatching\)\s*ContinueWatchingCardShared\(\)\s*Spacer\(modifier = Modifier\.height\(24\.dp\)\)', history_ui_movies.strip() + "\n", content)
content = content.replace("import androidx.compose.foundation.lazy.items", "import androidx.compose.foundation.lazy.items\nimport androidx.compose.foundation.lazy.LazyRow")

with open("app/src/main/java/com/example/ui/screens/movies/MoviesScreen.kt", "w") as f:
    f.write(content)


# SeriesScreen
with open("app/src/main/java/com/example/ui/screens/series/SeriesScreen.kt", "r") as f:
    content = f.read()

if "historyItems" not in content:
    content = content.replace("val downloadRepository = remember { DownloadRepository(context) }", "val historyRepository = remember { com.example.data.repository.HistoryRepository(context) }\n    val downloadRepository = remember { DownloadRepository(context) }\n" + history_state_series)

content = re.sub(r'SectionTitleShared\("Continue Watching", onSeeAllClick = onNavigateToWatching\)\s*ContinueWatchingCardShared\(\)\s*Spacer\(modifier = Modifier\.height\(24\.dp\)\)', history_ui_series.strip() + "\n", content)
content = content.replace("import androidx.compose.foundation.lazy.items", "import androidx.compose.foundation.lazy.items\nimport androidx.compose.foundation.lazy.LazyRow")

with open("app/src/main/java/com/example/ui/screens/series/SeriesScreen.kt", "w") as f:
    f.write(content)

