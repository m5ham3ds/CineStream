import re

with open("app/src/main/java/com/example/ui/screens/home/HomeScreen.kt", "r") as f:
    content = f.read()

parts = content.split("// Trending Now")
if len(parts) > 1:
    before = parts[0]
    after = "// Trending Now" + parts[1]
    
    parts2 = after.split("if (showBottomSheet) {")
    normal_content = parts2[0]
    bottom_sheet = "if (showBottomSheet) {" + parts2[1]
    
    grid_logic = """
        if (selectedCategory == "Home") {
""" + normal_content + """
        } else {
            val displayItems = when (selectedCategory) {
                "Movies" -> uiState.allMovies
                "Series" -> uiState.allSeries
                "Anime" -> uiState.animeSeries
                "Documentaries" -> uiState.allMovies.filter { it.genres.contains("Documentary") }
                else -> emptyList()
            }
            
            com.example.ui.components.VerticalGrid(
                items = displayItems,
                columns = 3,
                modifier = Modifier.padding(horizontal = 16.dp)
            ) { item ->
                // Because displayItems can be Movie or Series, we need to handle both
                // We'll just cast check since Kotlin supports it
                if (item is com.example.domain.models.Movie) {
                    MediaCard(
                        title = item.title,
                        posterUrl = item.posterUrl,
                        rank = null,
                        rating = item.rating,
                        year = item.year.toString(),
                        isMovie = true,
                        mediaId = item.id,
                        onClick = { onMovieClick(item.id) },
                        onLongClick = { 
                            bottomSheetIsMovie = true
                            selectedMediaId = item.id
                            selectedMediaTitle = item.title
                            selectedMediaPoster = item.posterUrl
                            showBottomSheet = true
                        }
                    )
                } else if (item is com.example.domain.models.Series) {
                    MediaCard(
                        title = item.title,
                        posterUrl = item.posterUrl,
                        rank = null,
                        rating = item.rating,
                        year = item.year.toString(),
                        isMovie = false,
                        mediaId = item.id,
                        onClick = { onSeriesClick(item.id) },
                        onLongClick = { 
                            bottomSheetIsMovie = false
                            selectedMediaId = item.id
                            selectedMediaTitle = item.title
                            selectedMediaPoster = item.posterUrl
                            showBottomSheet = true
                        }
                    )
                }
            }
        }
"""
    new_content = before + grid_logic + bottom_sheet
    
    if 'import com.example.ui.components.VerticalGrid' not in new_content:
        new_content = new_content.replace('import com.example.ui.components.MediaCard', 'import com.example.ui.components.MediaCard\nimport com.example.ui.components.VerticalGrid')
        
    with open("app/src/main/java/com/example/ui/screens/home/HomeScreen.kt", "w") as f:
        f.write(new_content)
