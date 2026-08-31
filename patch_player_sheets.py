import re

with open("app/src/main/java/com/example/ui/screens/player/PlayerScreen.kt", "r") as f:
    content = f.read()

state_vars = """    var isLocked by remember { mutableStateOf(false) }
    var currentSpeed by remember { mutableStateOf(1f) }
    var currentQuality by remember { mutableStateOf("1080p") }
    var showQualitySheet by remember { mutableStateOf(false) }
    var showEpisodesSheet by remember { mutableStateOf(false) }"""
content = content.replace("    var isLocked by remember { mutableStateOf(false) }", state_vars)

# Fix speed action
speed_target = """BottomAction(icon = Icons.Default.Speed, text = "Speed (1x)") { 
                                val newSpeed = if (exoPlayer.playbackParameters.speed == 1f) 1.5f else 1f
                                exoPlayer.setPlaybackSpeed(newSpeed)
                            }"""
speed_replacement = """BottomAction(icon = Icons.Default.Speed, text = "Speed (${currentSpeed}x)") { 
                                val nextSpeed = when(currentSpeed) {
                                    0.5f -> 1f
                                    1f -> 1.5f
                                    1.5f -> 2f
                                    else -> 0.5f
                                }
                                currentSpeed = nextSpeed
                                exoPlayer.setPlaybackSpeed(nextSpeed)
                            }"""
content = content.replace(speed_target, speed_replacement)

# Fix episodes action
episodes_target = """BottomAction(icon = Icons.Default.VideoLibrary, text = "Episodes") { }"""
episodes_replacement = """BottomAction(icon = Icons.Default.VideoLibrary, text = "Episodes") { showEpisodesSheet = true }"""
content = content.replace(episodes_target, episodes_replacement)

# Fix quality action
quality_target = """QualityAction(onClick = { })"""
quality_replacement = """QualityAction(currentQuality, onClick = { showQualitySheet = true })"""
content = content.replace(quality_target, quality_replacement)

# Fix QualityAction component signature
qa_target = """fun QualityAction(onClick: () -> Unit) {"""
qa_replacement = """fun QualityAction(currentQuality: String, onClick: () -> Unit) {"""
content = content.replace(qa_target, qa_replacement)

qa_body_target = """Text("1080p", color = Color(0xFFE50914), fontSize = 12.sp, fontWeight = FontWeight.Bold)"""
qa_body_replacement = """Text(currentQuality, color = Color(0xFFE50914), fontSize = 12.sp, fontWeight = FontWeight.Bold)"""
content = content.replace(qa_body_target, qa_body_replacement)

# Add sheets at the bottom of PlayerScreen before the custom Slider
sheets_code = """
    if (showQualitySheet) {
        ModalBottomSheet(
            onDismissRequest = { showQualitySheet = false },
            containerColor = Color(0xFF1C1C1E)
        ) {
            Column(modifier = Modifier.padding(16.dp)) {
                Text("Select Quality", color = Color.White, fontSize = 20.sp, fontWeight = FontWeight.Bold)
                Spacer(modifier = Modifier.height(16.dp))
                val qualities = listOf("4K", "1080p", "720p", "480p", "360p")
                qualities.forEach { q ->
                    TextButton(
                        onClick = { 
                            currentQuality = q
                            showQualitySheet = false
                        },
                        modifier = Modifier.fillMaxWidth()
                    ) {
                        Text(q, color = if (q == currentQuality) Color(0xFFE50914) else Color.White)
                    }
                }
                Spacer(modifier = Modifier.height(32.dp))
            }
        }
    }
    
    if (showEpisodesSheet) {
        ModalBottomSheet(
            onDismissRequest = { showEpisodesSheet = false },
            containerColor = Color(0xFF1C1C1E)
        ) {
            Column(modifier = Modifier.padding(16.dp)) {
                Text("Episodes", color = Color.White, fontSize = 20.sp, fontWeight = FontWeight.Bold)
                Spacer(modifier = Modifier.height(16.dp))
                LazyColumn {
                    items(5) { i ->
                        val epNum = i + 1
                        TextButton(
                            onClick = { showEpisodesSheet = false },
                            modifier = Modifier.fillMaxWidth()
                        ) {
                            Text("Episode $epNum", color = Color.White)
                        }
                    }
                }
                Spacer(modifier = Modifier.height(32.dp))
            }
        }
    }
"""
# Insert before 'DisposableEffect' or at the end of PlayerScreen body.
# Better to insert right before 'if (showDownloadSheet)'
content = content.replace("    if (showDownloadSheet) {", sheets_code + "\n    if (showDownloadSheet) {")

with open("app/src/main/java/com/example/ui/screens/player/PlayerScreen.kt", "w") as f:
    f.write(content)
