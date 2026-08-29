import re

files = [
    'app/src/main/java/com/example/ui/screens/details/DetailsScreens.kt'
]

for file_path in files:
    with open(file_path, 'r') as f:
        content = f.read()

    # Add import
    if 'import com.example.utils.SiteVerificationManager' not in content:
        content = content.replace('import androidx.compose.ui.unit.sp', 'import androidx.compose.ui.unit.sp\nimport com.example.utils.SiteVerificationManager')

    # Replace onSourceSelected for Movie
    old_on_source = """                    onSourceSelected = { source ->
                        showSourceSheet = false
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
                                    HistoryItem(
                                        id = movie.id,
                                        title = movie.title,
                                        posterUrl = movie.posterUrl,
                                        isMovie = true
                                    )
                                )
                                onPlay(source.url)
                            }
                        }
                    }"""
    
    new_on_source = """                    onSourceSelected = { source ->
                        if (!SiteVerificationManager.isVerificationComplete && SiteVerificationManager.verifiedSites.none { source.url.contains(it) || it.contains(source.providerName) }) {
                            Toast.makeText(context, "عملية تحديث البيانات لا تزال جارية، يرجى الانتظار...", Toast.LENGTH_SHORT).show()
                        } else {
                            showSourceSheet = false
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
                                        HistoryItem(
                                            id = movie.id,
                                            title = movie.title,
                                            posterUrl = movie.posterUrl,
                                            isMovie = true
                                        )
                                    )
                                    onPlay(source.url)
                                }
                            }
                        }
                    }"""
    
    content = content.replace(old_on_source, new_on_source)

    # Replace onSourceSelected for Series
    old_on_source_series = """                    onSourceSelected = { source ->
                        showSourceSheet = false
                        if (isDownloadMode) {
                            scope.launch {
                                downloadRepository.addToDownloads(DownloadItem(
                                    id = series.id, title = series.title, posterUrl = series.posterUrl, isMovie = false, quality = source.quality
                                ))
                                Toast.makeText(context, "Download Started: ${source.providerName}", Toast.LENGTH_SHORT).show()
                            }
                        } else {
                            scope.launch {
                                historyRepository.addToHistory(
                                    HistoryItem(
                                        id = series.id,
                                        title = series.title,
                                        posterUrl = series.posterUrl,
                                        isMovie = false
                                    )
                                )
                                onPlay(source.url)
                            }
                        }
                    }"""
    
    new_on_source_series = """                    onSourceSelected = { source ->
                        if (!SiteVerificationManager.isVerificationComplete && SiteVerificationManager.verifiedSites.none { source.url.contains(it) || it.contains(source.providerName) }) {
                            Toast.makeText(context, "عملية تحديث البيانات لا تزال جارية، يرجى الانتظار...", Toast.LENGTH_SHORT).show()
                        } else {
                            showSourceSheet = false
                            if (isDownloadMode) {
                                scope.launch {
                                    downloadRepository.addToDownloads(DownloadItem(
                                        id = series.id, title = series.title, posterUrl = series.posterUrl, isMovie = false, quality = source.quality
                                    ))
                                    Toast.makeText(context, "Download Started", Toast.LENGTH_SHORT).show()
                                }
                            } else {
                                scope.launch {
                                    historyRepository.addToHistory(
                                        HistoryItem(
                                            id = series.id,
                                            title = series.title,
                                            posterUrl = series.posterUrl,
                                            isMovie = false
                                        )
                                    )
                                    onPlay(source.url)
                                }
                            }
                        }
                    }"""
    
    content = content.replace(old_on_source_series, new_on_source_series)

    with open(file_path, 'w') as f:
        f.write(content)
