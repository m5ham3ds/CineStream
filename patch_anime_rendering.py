import re

with open("app/src/main/java/com/example/ui/screens/anime/AnimeScreen.kt", "r") as f:
    content = f.read()

# We want to wrap the sections starting from `if (animeHistoryItems.isNotEmpty())` to the end of the sections
# in a `if (selectedCategory == "Anime") { ... } else { ... }`

parts = content.split("if (animeHistoryItems.isNotEmpty()) {")
if len(parts) > 1:
    before = parts[0]
    after = "if (animeHistoryItems.isNotEmpty()) {" + parts[1]
    
    # Where does the normal content end?
    # Right before `if (showBottomSheet) {`
    parts2 = after.split("if (showBottomSheet) {")
    normal_content = parts2[0]
    bottom_sheet = "if (showBottomSheet) {" + parts2[1]
    
    # Strip trailing whitespace and braces properly.
    # The normal_content ends with some spaces and probably `    }\n    \n`
    # Let's just wrap it nicely.
    
    grid_logic = """
        import com.example.ui.components.VerticalGrid
        
        if (selectedCategory == "Anime") {
""" + normal_content + """
        } else {
            val displayItems = when (selectedCategory) {
                "New Releases" -> uiState.series.reversed()
                "Top Rated" -> uiState.series.sortedByDescending { it.rating }
                "Genres" -> uiState.series.shuffled() // Placeholder for genres
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
                    onClick = { onAnimeClick(series.id) },
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
    
    # We also need to remove the extra 'import' if it was added in the middle
    new_content = new_content.replace('        import com.example.ui.components.VerticalGrid', '')
    if 'import com.example.ui.components.VerticalGrid' not in new_content:
        new_content = new_content.replace('import com.example.ui.components.MediaCard', 'import com.example.ui.components.MediaCard\nimport com.example.ui.components.VerticalGrid')
        
    with open("app/src/main/java/com/example/ui/screens/anime/AnimeScreen.kt", "w") as f:
        f.write(new_content)
