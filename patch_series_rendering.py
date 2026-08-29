import re

with open("app/src/main/java/com/example/ui/screens/series/SeriesScreen.kt", "r") as f:
    content = f.read()

parts = content.split("if (seriesHistoryItems.isNotEmpty()) {")
if len(parts) > 1:
    before = parts[0]
    after = "if (seriesHistoryItems.isNotEmpty()) {" + parts[1]
    
    parts2 = after.split("if (showBottomSheet) {")
    normal_content = parts2[0]
    bottom_sheet = "if (showBottomSheet) {" + parts2[1]
    
    grid_logic = """
        if (selectedCategory == "Series") {
""" + normal_content + """
        } else {
            val displayItems = when (selectedCategory) {
                "New Releases" -> uiState.series.reversed()
                "Top Rated" -> uiState.series.sortedByDescending { it.rating }
                "Genres" -> uiState.series.shuffled()
                else -> uiState.series
            }
            
            com.example.ui.components.VerticalGrid(
                items = displayItems,
                columns = 3,
                modifier = Modifier.padding(horizontal = 16.dp)
            ) { series ->
                MediaCard(
                    title = series.title,
                    posterUrl = series.posterUrl,
                    rank = null,
                    rating = series.rating,
                    year = series.year.toString(),
                    isMovie = false,
                    mediaId = series.id,
                    onClick = { onSeriesClick(series.id) },
                    onLongClick = { 
                        selectedMediaId = series.id
                        selectedMediaTitle = series.title
                        selectedMediaPoster = series.posterUrl
                        showBottomSheet = true
                    }
                )
            }
        }
"""
    new_content = before + grid_logic + bottom_sheet
    
    if 'import com.example.ui.components.VerticalGrid' not in new_content:
        new_content = new_content.replace('import com.example.ui.components.MediaCard', 'import com.example.ui.components.MediaCard\nimport com.example.ui.components.VerticalGrid')
        
    with open("app/src/main/java/com/example/ui/screens/series/SeriesScreen.kt", "w") as f:
        f.write(new_content)
