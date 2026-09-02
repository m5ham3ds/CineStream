import re

with open("app/src/main/java/com/example/ui/screens/details/DetailsScreens.kt", "r") as f:
    content = f.read()

# 1. Add selectedTrailerId state to SeriesDetailsScreen
state_old = """    var showBatchDownloadSheet by remember { mutableStateOf(false) }

    LaunchedEffect(seriesId) {"""

state_new = """    var showBatchDownloadSheet by remember { mutableStateOf(false) }
    var selectedTrailerId by remember { mutableStateOf<String?>(null) }

    LaunchedEffect(seriesId) {"""

content = content.replace(state_old, state_new)

# 2. Replace the poster display with the inline player logic
poster_old = """                Box(modifier = Modifier.fillMaxWidth().height(400.dp)) {
                    AsyncImage(
                        model = series.posterUrl,
                        contentDescription = series.title,
                        contentScale = ContentScale.Crop,
                        modifier = Modifier.fillMaxSize()
                    )
                    Box(modifier = Modifier.fillMaxSize().background(Brush.verticalGradient(colors = listOf(Color.Transparent, MaterialTheme.colorScheme.background), startY = 300f)))
                    IconButton(onClick = onBack, modifier = Modifier.align(Alignment.TopStart).padding(16.dp).background(Color.Black.copy(alpha=0.5f), CircleShape)) {
                        Icon(Icons.AutoMirrored.Filled.ArrowBack, contentDescription = "Back", tint = Color.White)
                    }
                }
                Column(modifier = Modifier.padding(16.dp)) {"""

poster_new = """                if (selectedTrailerId != null) {
                    Box(modifier = Modifier.fillMaxWidth().aspectRatio(16f/9f)) {
                        com.example.ui.components.InlineYouTubePlayer(
                            videoId = selectedTrailerId!!,
                            modifier = Modifier.fillMaxSize()
                        )
                    }
                    Spacer(modifier = Modifier.height(16.dp))
                    Column(modifier = Modifier.padding(horizontal = 16.dp)) {
                } else {
                    Box(modifier = Modifier.fillMaxWidth().height(400.dp)) {
                        AsyncImage(
                            model = series.posterUrl,
                            contentDescription = series.title,
                            contentScale = ContentScale.Crop,
                            modifier = Modifier.fillMaxSize()
                        )
                        Box(modifier = Modifier.fillMaxSize().background(Brush.verticalGradient(colors = listOf(Color.Transparent, MaterialTheme.colorScheme.background), startY = 300f)))
                        IconButton(onClick = onBack, modifier = Modifier.align(Alignment.TopStart).padding(16.dp).background(Color.Black.copy(alpha=0.5f), CircleShape)) {
                            Icon(Icons.AutoMirrored.Filled.ArrowBack, contentDescription = "Back", tint = Color.White)
                        }
                    }
                    Column(modifier = Modifier.padding(16.dp)) {
                }"""

content = content.replace(poster_old, poster_new)

# 3. Update the TrailerCard onClick
trailer_old = """                                TrailerCard(trailer) { onPlay(series.title, "trailer:${trailer.key}") }"""
trailer_new = """                                TrailerCard(trailer) { selectedTrailerId = trailer.key }"""

content = content.replace(trailer_old, trailer_new)

with open("app/src/main/java/com/example/ui/screens/details/DetailsScreens.kt", "w") as f:
    f.write(content)

