import re

with open("app/src/main/java/com/example/ui/screens/details/DetailsScreens.kt", "r") as f:
    content = f.read()

# Add new imports
imports_to_add = """import com.example.ui.components.SourceSelectionSheet
import com.example.domain.providers.VideoSource
"""
content = content.replace("import kotlinx.coroutines.launch\n", "import kotlinx.coroutines.launch\n" + imports_to_add)


# Replace Movie Details Play logic
movie_play_logic_old = """                    var showDownloadSheet by remember { mutableStateOf(false) }

                    Row(
                        modifier = Modifier.fillMaxWidth(),
                        horizontalArrangement = Arrangement.spacedBy(16.dp),
                        verticalAlignment = Alignment.CenterVertically
                    ) {
                        Button(
                            onClick = { onPlay(defaultVideoUrl) },
                            modifier = Modifier.weight(1f)
                        ) {
                            Icon(Icons.Default.PlayArrow, contentDescription = "Play")
                            Spacer(modifier = Modifier.width(8.dp))
                            Text("Play")
                        }"""

movie_play_logic_new = """                    var showDownloadSheet by remember { mutableStateOf(false) }
                    var showSourceSheet by remember { mutableStateOf(false) }
                    var isDownloadMode by remember { mutableStateOf(false) }

                    Row(
                        modifier = Modifier.fillMaxWidth(),
                        horizontalArrangement = Arrangement.spacedBy(16.dp),
                        verticalAlignment = Alignment.CenterVertically
                    ) {
                        Button(
                            onClick = { 
                                isDownloadMode = false
                                showSourceSheet = true 
                            },
                            modifier = Modifier.weight(1f)
                        ) {
                            Icon(Icons.Default.PlayArrow, contentDescription = "Play")
                            Spacer(modifier = Modifier.width(8.dp))
                            Text("Play")
                        }"""

content = content.replace(movie_play_logic_old, movie_play_logic_new)

movie_download_old = """                        } else {
                            IconButton(
                                onClick = { showDownloadSheet = true },
                                modifier = Modifier.background(MaterialTheme.colorScheme.surfaceVariant, shape = CircleShape)
                            ) {
                                Icon(Icons.Default.Download, contentDescription = "Download")
                            }
                        }"""

movie_download_new = """                        } else {
                            IconButton(
                                onClick = { 
                                    isDownloadMode = true
                                    showSourceSheet = true 
                                },
                                modifier = Modifier.background(MaterialTheme.colorScheme.surfaceVariant, shape = CircleShape)
                            ) {
                                Icon(Icons.Default.Download, contentDescription = "Download")
                            }
                        }"""

content = content.replace(movie_download_old, movie_download_new)


# Now fix the sheets at the end of the Row
movie_sheets_old = """                    if (showDownloadSheet) {
                        DownloadQualitySheet(
                            onDismiss = { showDownloadSheet = false },
                            onQualitySelected = { quality ->
                                uiState.movie?.let { movie ->
                                    scope.launch {
                                        downloadRepository.addToDownloads(DownloadItem(
                                            id = movie.id, title = movie.title, posterUrl = movie.posterUrl, isMovie = true, quality = quality
                                        ))
                                        Toast.makeText(context, "Download Started", Toast.LENGTH_SHORT).show()
                                        showDownloadSheet = false
                                    }
                                }
                            }
                        )
                    }"""

movie_sheets_new = """                    if (showSourceSheet) {
                        SourceSelectionSheet(
                            mediaId = movie.id,
                            isMovie = true,
                            onDismiss = { showSourceSheet = false },
                            onSourceSelected = { source ->
                                showSourceSheet = false
                                if (isDownloadMode) {
                                    scope.launch {
                                        downloadRepository.addToDownloads(DownloadItem(
                                            id = movie.id, title = movie.title, posterUrl = movie.posterUrl, isMovie = true, quality = source.quality
                                        ))
                                        Toast.makeText(context, "Download Started: ${source.name}", Toast.LENGTH_SHORT).show()
                                    }
                                } else {
                                    onPlay(source.url)
                                }
                            }
                        )
                    }"""

content = content.replace(movie_sheets_old, movie_sheets_new)


# Series Details logic replacement
series_play_logic_old = """                    var showDownloadSheet by remember { mutableStateOf(false) }

                    Row(
                        modifier = Modifier.fillMaxWidth(),
                        horizontalArrangement = Arrangement.spacedBy(16.dp),
                        verticalAlignment = Alignment.CenterVertically
                    ) {
                        Button(
                            onClick = { onPlay(defaultVideoUrl) },
                            modifier = Modifier.weight(1f)
                        ) {
                            Icon(Icons.Default.PlayArrow, contentDescription = "Play")
                            Spacer(modifier = Modifier.width(8.dp))
                            Text("Resume")
                        }"""

series_play_logic_new = """                    var showDownloadSheet by remember { mutableStateOf(false) }
                    var showSourceSheet by remember { mutableStateOf(false) }
                    var isDownloadMode by remember { mutableStateOf(false) }

                    Row(
                        modifier = Modifier.fillMaxWidth(),
                        horizontalArrangement = Arrangement.spacedBy(16.dp),
                        verticalAlignment = Alignment.CenterVertically
                    ) {
                        Button(
                            onClick = { 
                                isDownloadMode = false
                                showSourceSheet = true 
                            },
                            modifier = Modifier.weight(1f)
                        ) {
                            Icon(Icons.Default.PlayArrow, contentDescription = "Play")
                            Spacer(modifier = Modifier.width(8.dp))
                            Text("Resume")
                        }"""

content = content.replace(series_play_logic_old, series_play_logic_new)

series_sheets_old = """                    if (showDownloadSheet) {
                        DownloadQualitySheet(
                            onDismiss = { showDownloadSheet = false },
                            onQualitySelected = { quality ->
                                uiState.series?.let { series ->
                                    scope.launch {
                                        downloadRepository.addToDownloads(DownloadItem(
                                            id = series.id, title = series.title, posterUrl = series.posterUrl, isMovie = false, quality = quality
                                        ))
                                        Toast.makeText(context, "Download Started", Toast.LENGTH_SHORT).show()
                                        showDownloadSheet = false
                                    }
                                }
                            }
                        )
                    }"""

series_sheets_new = """                    if (showSourceSheet) {
                        SourceSelectionSheet(
                            mediaId = series.id,
                            isMovie = false,
                            onDismiss = { showSourceSheet = false },
                            onSourceSelected = { source ->
                                showSourceSheet = false
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
                            }
                        )
                    }"""

content = content.replace(series_sheets_old, series_sheets_new)

with open("app/src/main/java/com/example/ui/screens/details/DetailsScreens.kt", "w") as f:
    f.write(content)
