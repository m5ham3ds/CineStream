import re

with open("app/src/main/java/com/example/ui/screens/movies/MoviesScreen.kt", "r") as f:
    content = f.read()

parts = content.split("if (movieHistoryItems.isNotEmpty()) {")
if len(parts) > 1:
    before = parts[0]
    after = "if (movieHistoryItems.isNotEmpty()) {" + parts[1]
    
    parts2 = after.split("if (showBottomSheet) {")
    normal_content = parts2[0]
    bottom_sheet = "if (showBottomSheet) {" + parts2[1]
    
    grid_logic = """
        if (selectedCategory == "Movies") {
""" + normal_content + """
        } else {
            val displayItems = when (selectedCategory) {
                "New Releases" -> uiState.movies.reversed()
                "Top Rated" -> uiState.movies.sortedByDescending { it.rating }
                "Genres" -> uiState.movies.shuffled() // Placeholder for genres
                else -> uiState.movies
            }
            
            com.example.ui.components.VerticalGrid(
                items = displayItems,
                columns = 3,
                modifier = Modifier.padding(horizontal = 16.dp)
            ) { movie ->
                MediaCard(
                    title = movie.title,
                    posterUrl = movie.posterUrl,
                    rank = null,
                    rating = movie.rating,
                    year = movie.year.toString(),
                    isMovie = true,
                    mediaId = movie.id,
                    onClick = { onMovieClick(movie.id) },
                    onLongClick = { 
                        selectedMediaId = movie.id
                        selectedMediaTitle = movie.title
                        selectedMediaPoster = movie.posterUrl
                        showBottomSheet = true
                    }
                )
            }
        }
"""
    new_content = before + grid_logic + bottom_sheet
    
    if 'import com.example.ui.components.VerticalGrid' not in new_content:
        new_content = new_content.replace('import com.example.ui.components.MediaCard', 'import com.example.ui.components.MediaCard\nimport com.example.ui.components.VerticalGrid')
        
    with open("app/src/main/java/com/example/ui/screens/movies/MoviesScreen.kt", "w") as f:
        f.write(new_content)
