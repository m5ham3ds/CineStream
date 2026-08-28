import re

with open("app/src/main/java/com/example/ui/screens/details/DetailsScreens.kt", "r") as f:
    content = f.read()

# Just replace `var showDownloadSheet by remember { mutableStateOf(false) }` globally with all three
old_vars = "var showDownloadSheet by remember { mutableStateOf(false) }"
new_vars = """var showDownloadSheet by remember { mutableStateOf(false) }
                    var showSourceSheet by remember { mutableStateOf(false) }
                    var isDownloadMode by remember { mutableStateOf(false) }"""

content = content.replace(old_vars, new_vars)

# Also fix the Play button for MovieDetailsScreen that missed the first replacement
old_movie_play = """                        Button(
                            onClick = { onPlay(defaultVideoUrl) },
                            modifier = Modifier.weight(1f)
                        ) {
                            Icon(Icons.Default.PlayArrow, contentDescription = "Play")
                            Spacer(modifier = Modifier.width(8.dp))
                            Text("Play")
                        }"""
new_movie_play = """                        Button(
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
content = content.replace(old_movie_play, new_movie_play)

with open("app/src/main/java/com/example/ui/screens/details/DetailsScreens.kt", "w") as f:
    f.write(content)
