import re

with open('app/src/main/java/com/example/ui/screens/details/DetailsScreens.kt', 'r') as f:
    content = f.read()

# I will replace everything from '@OptIn(ExperimentalMaterial3Api::class)\n@Composable\nfun SeriesDetailsScreen' to the end of the file.

split_str = '@OptIn(ExperimentalMaterial3Api::class)\n@Composable\nfun SeriesDetailsScreen'
if split_str in content:
    before = content.split(split_str)[0]
    
    new_content = before + """@OptIn(ExperimentalMaterial3Api::class, androidx.compose.foundation.ExperimentalFoundationApi::class)
@Composable
fun SeriesDetailsScreen(
    onPersonClick: (String) -> Unit = {},
    seriesId: String,
    onBack: () -> Unit,
    onPlay: (String) -> Unit
) {
    val context = LocalContext.current
    val viewModel: SeriesDetailsViewModel = viewModel(factory = ViewModelFactory())
    val uiState by viewModel.uiState.collectAsState()
    val scope = rememberCoroutineScope()
    val libraryRepository = remember { LibraryRepository(context) }
    val isFavorite by libraryRepository.isLibraryItem(seriesId).collectAsState(initial = false)
    val downloadRepository = remember { DownloadRepository(context) }
    val historyRepository = remember { com.example.data.repository.HistoryRepository(context) }
    val watchedRepo = remember { com.example.data.repository.WatchedEpisodeRepository(context) }
    val watchedEpisodes by watchedRepo.getAllWatched().collectAsState(initial = emptyList())
    val watchedEpisodeIds = watchedEpisodes.map { it.id }.toSet()

    var selectedEpisodeForSource by remember { mutableStateOf<Episode?>(null) }
    var isDownloadMode by remember { mutableStateOf(false) }
    var showBatchDownloadSheet by remember { mutableStateOf(false) }

    LaunchedEffect(seriesId) {
        viewModel.loadSeries(seriesId)
    }

    val pullRefreshState = rememberPullToRefreshState()
    PullToRefreshBox(
        isRefreshing = uiState.isLoading,
        onRefresh = { viewModel.loadSeries(seriesId) },
        state = pullRefreshState
    ) {
        val series = uiState.series
        if (series == null && !uiState.isLoading) {
            Box(modifier = Modifier.fillMaxSize(), contentAlignment = Alignment.Center) {
                Text(uiState.error ?: "Failed to load details", color = MaterialTheme.colorScheme.error)
            }
            return@PullToRefreshBox
        }

        if (series != null) {
            val scrollState = rememberScrollState()
            Column(
                modifier = Modifier
                    .fillMaxSize()
                    .verticalScroll(scrollState)
            ) {
                Box(modifier = Modifier.fillMaxWidth().height(400.dp)) {
                    AsyncImage(
                        model = series.posterUrl,
                        contentDescription = series.title,
                        contentScale = ContentScale.Crop,
                        modifier = Modifier.fillMaxSize()
                    )
                    Box(
                        modifier = Modifier
                            .fillMaxSize()
                            .background(
                                Brush.verticalGradient(
                                    colors = listOf(Color.Transparent, MaterialTheme.colorScheme.background),
                                    startY = 300f
                                )
                            )
                    )
                }

                Column(modifier = Modifier.padding(16.dp)) {
                    Text(series.title, style = MaterialTheme.typography.headlineMedium, fontWeight = FontWeight.Bold, color = MaterialTheme.colorScheme.onBackground)
                    Spacer(modifier = Modifier.height(8.dp))
                    Row(verticalAlignment = Alignment.CenterVertically) {
                        Icon(Icons.Default.Star, contentDescription = "Rating", tint = Color(0xFFFFC107), modifier = Modifier.size(20.dp))
                        Spacer(modifier = Modifier.width(4.dp))
                        Text(String.format("%.1f", series.rating), style = MaterialTheme.typography.titleMedium, color = MaterialTheme.colorScheme.onBackground)
                        Spacer(modifier = Modifier.width(16.dp))
                        Text(series.year, style = MaterialTheme.typography.titleMedium, color = MaterialTheme.colorScheme.onSurfaceVariant)
                    }
                    Spacer(modifier = Modifier.height(16.dp))
                    
                    val firstUnplayedEpisode = uiState.episodes.firstOrNull { !watchedEpisodeIds.contains(it.id) } ?: uiState.episodes.firstOrNull()

                    // Action Buttons
                    Row(modifier = Modifier.fillMaxWidth(), horizontalArrangement = Arrangement.spacedBy(16.dp)) {
                        Button(
                            onClick = {
                                if (firstUnplayedEpisode != null) {
                                    selectedEpisodeForSource = firstUnplayedEpisode
                                    isDownloadMode = false
                                } else {
                                    Toast.makeText(context, "No episodes available", Toast.LENGTH_SHORT).show()
                                }
                            },
                            modifier = Modifier.weight(1f),
                            shape = RoundedCornerShape(8.dp)
                        ) {
                            Icon(Icons.Default.PlayArrow, contentDescription = "Play")
                            Spacer(modifier = Modifier.width(8.dp))
                            Text(stringResource(R.string.play))
                        }
                        IconButton(
                            onClick = {
                                showBatchDownloadSheet = true
                            },
                            modifier = Modifier.background(MaterialTheme.colorScheme.surfaceVariant, RoundedCornerShape(8.dp))
                        ) {
                            Icon(Icons.Default.Download, contentDescription = "Download")
                        }
                        IconButton(
                            onClick = {
                                scope.launch {
                                    if (isFavorite) {
                                        libraryRepository.removeFromLibrary(seriesId)
                                    } else {
                                        libraryRepository.addToLibrary(
                                            LibraryItem(
                                                id = series.id,
                                                title = series.title,
                                                posterUrl = series.posterUrl,
                                                isMovie = false
                                            )
                                        )
                                    }
                                }
                            },
                            modifier = Modifier.background(MaterialTheme.colorScheme.surfaceVariant, RoundedCornerShape(8.dp))
                        ) {
                            Icon(if (isFavorite) Icons.Default.Favorite else Icons.Default.FavoriteBorder, contentDescription = "Add to Favorites", tint = if (isFavorite) Color.Red else MaterialTheme.colorScheme.onBackground)
                        }
                    }

                    Spacer(modifier = Modifier.height(24.dp))
                    Text(series.overview, style = MaterialTheme.typography.bodyMedium, color = MaterialTheme.colorScheme.onBackground)
                    Spacer(modifier = Modifier.height(24.dp))

                    if (series.trailers.isNotEmpty()) {
                        Text(stringResource(R.string.trailers), color = MaterialTheme.colorScheme.onBackground, style = MaterialTheme.typography.titleMedium, fontWeight = FontWeight.Bold)
                        Spacer(modifier = Modifier.height(8.dp))
                        LazyRow(horizontalArrangement = Arrangement.spacedBy(16.dp)) {
                            items(series.trailers) { trailer ->
                                TrailerCard(trailer) { onPlay("trailer:${trailer.key}") }
                            }
                        }
                        Spacer(modifier = Modifier.height(32.dp))
                    }
                    if (series.cast.isNotEmpty()) {
                        Text(stringResource(R.string.cast), color = MaterialTheme.colorScheme.onBackground, style = MaterialTheme.typography.titleMedium, fontWeight = FontWeight.Bold)
                        Spacer(modifier = Modifier.height(8.dp))
                        LazyRow(horizontalArrangement = Arrangement.spacedBy(16.dp)) {
                            items(series.cast) { CastMemberCard(it) { onPersonClick(it.id) } }
                        }
                        Spacer(modifier = Modifier.height(32.dp))
                    }
                }

                // Seasons & Episodes
                if (series.seasons.isNotEmpty()) {
                    Text(stringResource(R.string.seasons_and_episodes), color = MaterialTheme.colorScheme.onBackground, style = MaterialTheme.typography.titleMedium, fontWeight = FontWeight.Bold, modifier = Modifier.padding(horizontal = 16.dp))
                    Spacer(modifier = Modifier.height(8.dp))
                    
                    // Season Tabs
                    LazyRow(contentPadding = PaddingValues(horizontal = 16.dp), horizontalArrangement = Arrangement.spacedBy(8.dp)) {
                        items(series.seasons.filter { it.seasonNumber > 0 }) { season ->
                            val isSelected = uiState.selectedSeason?.id == season.id
                            FilterChip(
                                selected = isSelected,
                                onClick = { viewModel.selectSeason(season) },
                                label = { Text(stringResource(R.string.season_number, season.seasonNumber)) },
                                colors = FilterChipDefaults.filterChipColors(
                                    selectedContainerColor = MaterialTheme.colorScheme.primary,
                                    selectedLabelColor = MaterialTheme.colorScheme.onBackground
                                )
                            )
                        }
                    }
                    Spacer(modifier = Modifier.height(16.dp))

                    // Episodes
                    if (uiState.isEpisodesLoading) {
                        Box(modifier = Modifier.fillMaxWidth().padding(32.dp), contentAlignment = Alignment.Center) { CircularProgressIndicator() }
                    } else {
                        uiState.episodes.forEach { episode ->
                            val isWatched = watchedEpisodeIds.contains(episode.id)
                            EpisodeCard(
                                episode = episode,
                                isWatched = isWatched,
                                onClick = {
                                    selectedEpisodeForSource = episode
                                    isDownloadMode = false
                                },
                                onLongClick = {
                                    scope.launch {
                                        if (isWatched) watchedRepo.markAsUnwatched(episode.id)
                                        else watchedRepo.markAsWatched(episode.id)
                                    }
                                },
                                onDownloadClick = {
                                    selectedEpisodeForSource = episode
                                    isDownloadMode = true
                                }
                            )
                        }
                    }
                    Spacer(modifier = Modifier.height(32.dp))
                }
            }
            
            if (selectedEpisodeForSource != null) {
                SourceSelectionSheet(
                    mediaId = series.id,
                    mediaTitle = "${series.title} S${selectedEpisodeForSource?.seasonNumber}E${selectedEpisodeForSource?.episodeNumber}",
                    isMovie = false,
                    episodeId = selectedEpisodeForSource?.id,
                    onDismiss = { selectedEpisodeForSource = null },
                    onSourceSelected = { source ->
                        val ep = selectedEpisodeForSource!!
                        selectedEpisodeForSource = null
                        if (isDownloadMode) {
                            scope.launch {
                                downloadRepository.addToDownloads(DownloadItem(
                                    id = ep.id, title = "${series.title} - S${ep.seasonNumber}E${ep.episodeNumber}", posterUrl = ep.thumbnailUrl, isMovie = false, quality = source.quality
                                ))
                                Toast.makeText(context, "Download Started: ${source.providerName}", Toast.LENGTH_SHORT).show()
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
                                watchedRepo.markAsWatched(ep.id)
                                onPlay(source.url)
                            }
                        }
                    }
                )
            }
            
            if (showBatchDownloadSheet) {
                com.example.ui.components.BatchDownloadSheet(
                    series = series,
                    currentSeason = uiState.selectedSeason,
                    episodes = uiState.episodes,
                    onDismiss = { showBatchDownloadSheet = false }
                )
            }

            IconButton(
                onClick = onBack,
                modifier = Modifier
                    .padding(top = WindowInsets.statusBars.asPaddingValues().calculateTopPadding() + 8.dp, start = 16.dp)
                    .background(Color.Black.copy(alpha=0.3f), CircleShape)
            ) {
                Icon(Icons.AutoMirrored.Filled.ArrowBack, contentDescription = "Back", tint = Color.White)
            }
        }
    }
}

@Composable
fun TrailerCard(trailer: VideoTrailer, onClick: () -> Unit) {
    Box(
        modifier = Modifier
            .width(200.dp)
            .aspectRatio(16f/9f)
            .clip(RoundedCornerShape(8.dp))
            .clickable { onClick() }
    ) {
        AsyncImage(
            model = "https://img.youtube.com/vi/${trailer.key}/hqdefault.jpg",
            contentDescription = trailer.name,
            contentScale = ContentScale.Crop,
            modifier = Modifier.fillMaxSize()
        )
        Box(modifier = Modifier.fillMaxSize().background(Color.Black.copy(alpha=0.3f)), contentAlignment = Alignment.Center) {
            Icon(Icons.Default.PlayArrow, contentDescription = "Play", tint = Color.White, modifier = Modifier.size(48.dp))
        }
        Text(
            text = trailer.name,
            color = Color.White,
            style = MaterialTheme.typography.labelSmall,
            maxLines = 1,
            overflow = TextOverflow.Ellipsis,
            modifier = Modifier.align(Alignment.BottomStart).padding(8.dp)
        )
    }
}

@Composable
fun CastMemberCard(cast: CastMember, onClick: () -> Unit) {
    Column(horizontalAlignment = Alignment.CenterHorizontally, modifier = Modifier.width(80.dp).clickable { onClick() }) {
        AsyncImage(
            model = cast.profileUrl ?: "https://via.placeholder.com/150",
            contentDescription = cast.name,
            contentScale = ContentScale.Crop,
            modifier = Modifier.size(72.dp).clip(CircleShape).background(Color.DarkGray)
        )
        Spacer(modifier = Modifier.height(8.dp))
        Text(cast.name, color = MaterialTheme.colorScheme.onBackground, style = MaterialTheme.typography.labelMedium, maxLines = 1, overflow = TextOverflow.Ellipsis)
        Text(cast.character, color = MaterialTheme.colorScheme.onSurfaceVariant, style = MaterialTheme.typography.labelSmall, maxLines = 1, overflow = TextOverflow.Ellipsis)
    }
}

@OptIn(androidx.compose.foundation.ExperimentalFoundationApi::class)
@Composable
fun EpisodeCard(
    episode: Episode,
    isWatched: Boolean,
    onClick: () -> Unit,
    onLongClick: () -> Unit,
    onDownloadClick: () -> Unit
) {
    Row(
        modifier = Modifier
            .fillMaxWidth()
            .combinedClickable(
                onClick = onClick,
                onLongClick = onLongClick
            )
            .padding(horizontal = 16.dp, vertical = 8.dp),
        verticalAlignment = Alignment.CenterVertically
    ) {
        Box(
            modifier = Modifier.width(120.dp).aspectRatio(16f/9f).clip(RoundedCornerShape(8.dp))
        ) {
            AsyncImage(
                model = episode.thumbnailUrl,
                contentDescription = episode.title,
                contentScale = ContentScale.Crop,
                modifier = Modifier.fillMaxSize().background(Color.DarkGray)
            )
            Icon(Icons.Default.PlayArrow, contentDescription = "Play", tint = Color.White, modifier = Modifier.align(Alignment.Center))
        }
        Spacer(modifier = Modifier.width(16.dp))
        Column(modifier = Modifier.weight(1f)) {
            Text(
                text = "${episode.episodeNumber}. ${episode.title}",
                color = if (isWatched) MaterialTheme.colorScheme.onBackground.copy(alpha = 0.5f) else MaterialTheme.colorScheme.onBackground,
                style = MaterialTheme.typography.titleMedium,
                fontWeight = FontWeight.Bold,
                maxLines = 1,
                overflow = TextOverflow.Ellipsis
            )
            Spacer(modifier = Modifier.height(4.dp))
            Row(verticalAlignment = Alignment.CenterVertically) {
                Icon(Icons.Default.Star, contentDescription = "Rating", tint = Color(0xFFFFC107), modifier = Modifier.size(12.dp))
                Spacer(modifier = Modifier.width(4.dp))
                Text(String.format("%.1f", episode.rating), color = MaterialTheme.colorScheme.onSurfaceVariant, style = MaterialTheme.typography.labelSmall)
                Spacer(modifier = Modifier.width(8.dp))
                Text("${episode.duration}m", color = MaterialTheme.colorScheme.onSurfaceVariant, style = MaterialTheme.typography.labelSmall)
            }
            Spacer(modifier = Modifier.height(4.dp))
            Text(episode.overview, color = MaterialTheme.colorScheme.onSurfaceVariant, style = MaterialTheme.typography.bodySmall, maxLines = 2, overflow = TextOverflow.Ellipsis)
        }
        IconButton(onClick = onDownloadClick) {
            Icon(Icons.Default.Download, contentDescription = "Download", tint = MaterialTheme.colorScheme.onBackground)
        }
    }
}
"""
    with open('app/src/main/java/com/example/ui/screens/details/DetailsScreens.kt', 'w') as f:
        f.write(new_content)
