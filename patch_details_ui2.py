import re

logic_movie = """
    val context = LocalContext.current
    val historyRepository = remember { com.example.data.repository.HistoryRepository(context) }
    
    LaunchedEffect(movie) {
        if (movie != null) {
            historyRepository.addToHistory(
                com.example.data.model.HistoryItem(
                    id = movie.id,
                    title = movie.title,
                    posterUrl = movie.posterUrl,
                    isMovie = true
                )
            )
        }
    }
"""

logic_series = """
    val context = LocalContext.current
    val historyRepository = remember { com.example.data.repository.HistoryRepository(context) }
    
    LaunchedEffect(series) {
        if (series != null) {
            historyRepository.addToHistory(
                com.example.data.model.HistoryItem(
                    id = series.id,
                    title = series.title,
                    posterUrl = series.posterUrl,
                    isMovie = false
                )
            )
        }
    }
"""

with open("app/src/main/java/com/example/ui/screens/details/DetailsScreens.kt", "r") as f:
    content = f.read()

content = content.replace("val movie = uiState.movie", logic_movie.strip() + "\n    val movie = uiState.movie")
content = content.replace("val series = uiState.series", logic_series.strip() + "\n    val series = uiState.series")

with open("app/src/main/java/com/example/ui/screens/details/DetailsScreens.kt", "w") as f:
    f.write(content)

