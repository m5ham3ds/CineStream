import re

with open("app/src/main/java/com/example/ui/screens/details/DetailsScreens.kt", "r") as f:
    content = f.read()

movie_old = """
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
    val movie = uiState.movie!!
"""

movie_new = """
            val movie = uiState.movie!!
            val ctx = LocalContext.current
            val historyRepository = remember { com.example.data.repository.HistoryRepository(ctx) }
            LaunchedEffect(movie) {
                historyRepository.addToHistory(
                    com.example.data.model.HistoryItem(
                        id = movie.id,
                        title = movie.title,
                        posterUrl = movie.posterUrl,
                        isMovie = true
                    )
                )
            }
"""

series_old = """
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
    val series = uiState.series!!
"""

series_new = """
            val series = uiState.series!!
            val ctx = LocalContext.current
            val historyRepository = remember { com.example.data.repository.HistoryRepository(ctx) }
            LaunchedEffect(series) {
                historyRepository.addToHistory(
                    com.example.data.model.HistoryItem(
                        id = series.id,
                        title = series.title,
                        posterUrl = series.posterUrl,
                        isMovie = false
                    )
                )
            }
"""

content = content.replace(movie_old.strip(), movie_new.strip())
content = content.replace(series_old.strip(), series_new.strip())

with open("app/src/main/java/com/example/ui/screens/details/DetailsScreens.kt", "w") as f:
    f.write(content)

