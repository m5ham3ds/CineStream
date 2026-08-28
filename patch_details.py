import re

with open("app/src/main/java/com/example/ui/screens/details/DetailsScreens.kt", "r") as f:
    content = f.read()

# Fix Movie history
movie_history = """
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
content = content.replace(movie_history, "")

movie_sheet = """
                        if (isDownloadMode) {
                            scope.launch {
                                downloadRepository.addToDownloads(DownloadItem(
                                    id = movie.id, title = movie.title, posterUrl = movie.posterUrl, isMovie = true, quality = source.quality
                                ))
                                Toast.makeText(context, "Download Started", Toast.LENGTH_SHORT).show()
                            }
                        } else {
                            onPlay(source.url)
                        }
"""
movie_sheet_new = """
                        if (isDownloadMode) {
                            scope.launch {
                                downloadRepository.addToDownloads(DownloadItem(
                                    id = movie.id, title = movie.title, posterUrl = movie.posterUrl, isMovie = true, quality = source.quality
                                ))
                                Toast.makeText(context, "Download Started", Toast.LENGTH_SHORT).show()
                            }
                        } else {
                            scope.launch {
                                historyRepository.addToHistory(
                                    com.example.data.model.HistoryItem(
                                        id = movie.id,
                                        title = movie.title,
                                        posterUrl = movie.posterUrl,
                                        isMovie = true
                                    )
                                )
                                onPlay(source.url)
                            }
                        }
"""
content = content.replace(movie_sheet, movie_sheet_new)


# Fix Series history
series_history = """
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
content = content.replace(series_history, "")

series_sheet = """
                        if (isDownloadMode) {
                            scope.launch {
                                downloadRepository.addToDownloads(DownloadItem(
                                    id = series.id, title = series.title, posterUrl = series.posterUrl, isMovie = false, quality = source.quality
                                ))
                                Toast.makeText(context, "Download Started: ${source.name}", Toast.LENGTH_SHORT).show()
                            }
                        } else {
                            onPlay(source.url)
                        }
"""
series_sheet_new = """
                        if (isDownloadMode) {
                            scope.launch {
                                downloadRepository.addToDownloads(DownloadItem(
                                    id = series.id, title = series.title, posterUrl = series.posterUrl, isMovie = false, quality = source.quality
                                ))
                                Toast.makeText(context, "Download Started: ${source.name}", Toast.LENGTH_SHORT).show()
                            }
                        } else {
                            scope.launch {
                                historyRepository.addToHistory(
                                    com.example.data.model.HistoryItem(
                                        id = series.id,
                                        title = series.title,
                                        posterUrl = series.posterUrl,
                                        isMovie = false
                                    )
                                )
                                onPlay(source.url)
                            }
                        }
"""
content = content.replace(series_sheet, series_sheet_new)


# Fix padding for Movie
content = content.replace(
    "modifier = Modifier.fillMaxSize().padding(padding)",
    "modifier = Modifier.fillMaxSize().padding(bottom = padding.calculateBottomPadding())",
    1 # Only the first one (movie)
)

# Fix padding for Series
content = content.replace(
    "modifier = Modifier.fillMaxSize().padding(padding)",
    "modifier = Modifier.fillMaxSize().padding(bottom = padding.calculateBottomPadding())"
)


with open("app/src/main/java/com/example/ui/screens/details/DetailsScreens.kt", "w") as f:
    f.write(content)
