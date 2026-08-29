import re

with open('app/src/main/java/com/example/ui/screens/details/DetailsScreens.kt', 'r') as f:
    content = f.read()

# For MovieDetailsScreen
# 1. Replace isDownloaded with downloadItem logic
content = re.sub(r'val isDownloaded = downloadItems.any \{ it.id == movieId \}',
    r'val downloadItem = downloadItems.find { it.id == movieId }\n    var showDeleteConfirm by remember { mutableStateOf(false) }', content)

# 2. Add Delete Confirm dialog inside the main Column, just before Hero Image
movie_dialog = """
                if (showDeleteConfirm) {
                    AlertDialog(
                        onDismissRequest = { showDeleteConfirm = false },
                        title = { Text("حذف التنزيل", color = Color.White) },
                        text = { Text("هل أنت متأكد أنك تريد حذف هذا العنصر من التنزيلات؟", color = Color.LightGray) },
                        confirmButton = {
                            TextButton(onClick = {
                                downloadItem?.let {
                                    scope.launch { downloadRepository.removeFromDownloads(it) }
                                }
                                showDeleteConfirm = false
                            }) { Text("نعم، احذف", color = Color.Red) }
                        },
                        dismissButton = {
                            TextButton(onClick = { showDeleteConfirm = false }) { Text("إلغاء", color = Color.White) }
                        },
                        containerColor = Color(0xFF161618)
                    )
                }
                
                // Hero Image or Video Player
"""
content = content.replace('// Hero Image or Video Player', movie_dialog, 1)

# 3. Update Download button in Movie
movie_download_button_old = """                    IconButton(
                        onClick = { isDownloadMode = true; showSourceSheet = true },
                        modifier = Modifier.size(50.dp).background(Color.DarkGray, CircleShape)
                    ) {
                        Icon(Icons.Default.Download, contentDescription = "Download", tint = if (isDownloaded) Color.Green else Color.White)
                    }"""

movie_download_button_new = """                    IconButton(
                        onClick = { 
                            if (downloadItem?.isCompleted == true) {
                                showDeleteConfirm = true
                            } else if (downloadItem == null) {
                                isDownloadMode = true
                                showSourceSheet = true
                            }
                        },
                        modifier = Modifier.size(50.dp).background(Color.DarkGray, CircleShape)
                    ) {
                        if (downloadItem?.isCompleted == true) {
                            Icon(Icons.Default.DownloadDone, contentDescription = "Downloaded", tint = Color.Green)
                        } else if (downloadItem != null) {
                            CircularProgressIndicator(progress = { downloadItem.progress }, color = Color(0xFFE50914), modifier = Modifier.size(24.dp))
                        } else {
                            Icon(Icons.Default.Download, contentDescription = "Download", tint = Color.White)
                        }
                    }"""
content = content.replace(movie_download_button_old, movie_download_button_new)

# 4. Update Play Button in Movie
movie_play_old = """                    Button(
                        onClick = { isDownloadMode = false; showSourceSheet = true },
                        modifier = Modifier.weight(1f).height(50.dp),
                        colors = ButtonDefaults.buttonColors(containerColor = Color(0xFFE50914))
                    ) {
                        Icon(Icons.Default.PlayArrow, contentDescription = "Play", tint = Color.White)
                        Spacer(modifier = Modifier.width(8.dp))
                        Text("Play", color = Color.White, fontWeight = FontWeight.Bold)
                    }"""

movie_play_new = """                    Button(
                        onClick = { 
                            if (downloadItem?.isCompleted == true) {
                                onPlay("local_offline_file://${downloadItem.id}")
                            } else {
                                isDownloadMode = false; showSourceSheet = true 
                            }
                        },
                        modifier = Modifier.weight(1f).height(50.dp),
                        colors = ButtonDefaults.buttonColors(containerColor = Color(0xFFE50914))
                    ) {
                        Icon(Icons.Default.PlayArrow, contentDescription = "Play", tint = Color.White)
                        Spacer(modifier = Modifier.width(8.dp))
                        Text(if (downloadItem?.isCompleted == true) "Play Offline" else "Play", color = Color.White, fontWeight = FontWeight.Bold)
                    }"""
content = content.replace(movie_play_old, movie_play_new)

# For SeriesDetailsScreen
# 1. Replace isDownloaded with downloadItem logic
content = re.sub(r'val isDownloaded = downloadItems.any \{ it.id == seriesId \}',
    r'val downloadItem = downloadItems.find { it.id == seriesId }\n    var showDeleteConfirm by remember { mutableStateOf(false) }', content)

# 2. Add Delete Confirm dialog inside the main Column, just before Hero Image
series_dialog = """
                if (showDeleteConfirm) {
                    AlertDialog(
                        onDismissRequest = { showDeleteConfirm = false },
                        title = { Text("حذف التنزيل", color = Color.White) },
                        text = { Text("هل أنت متأكد أنك تريد حذف هذا العنصر من التنزيلات؟", color = Color.LightGray) },
                        confirmButton = {
                            TextButton(onClick = {
                                downloadItem?.let {
                                    scope.launch { downloadRepository.removeFromDownloads(it) }
                                }
                                showDeleteConfirm = false
                            }) { Text("نعم، احذف", color = Color.Red) }
                        },
                        dismissButton = {
                            TextButton(onClick = { showDeleteConfirm = false }) { Text("إلغاء", color = Color.White) }
                        },
                        containerColor = Color(0xFF161618)
                    )
                }
                
                // Hero Image or Video Player
"""
# Note: we need to replace the SECOND occurrence of '// Hero Image or Video Player' for series
parts = content.split('// Hero Image or Video Player')
if len(parts) == 3:
    content = parts[0] + '// Hero Image or Video Player' + parts[1] + series_dialog + parts[2]
else:
    print("Warning: could not find second Hero Image marker")

# 3. Update Download button in Series
series_download_button_old = """                    IconButton(
                        onClick = { isDownloadMode = true; showSourceSheet = true },
                        modifier = Modifier.size(50.dp).background(Color.DarkGray, CircleShape)
                    ) {
                        Icon(Icons.Default.Download, contentDescription = "Download", tint = if (isDownloaded) Color.Green else Color.White)
                    }"""

series_download_button_new = """                    IconButton(
                        onClick = { 
                            if (downloadItem?.isCompleted == true) {
                                showDeleteConfirm = true
                            } else if (downloadItem == null) {
                                isDownloadMode = true
                                showSourceSheet = true
                            }
                        },
                        modifier = Modifier.size(50.dp).background(Color.DarkGray, CircleShape)
                    ) {
                        if (downloadItem?.isCompleted == true) {
                            Icon(Icons.Default.DownloadDone, contentDescription = "Downloaded", tint = Color.Green)
                        } else if (downloadItem != null) {
                            CircularProgressIndicator(progress = { downloadItem.progress }, color = Color(0xFFE50914), modifier = Modifier.size(24.dp))
                        } else {
                            Icon(Icons.Default.Download, contentDescription = "Download", tint = Color.White)
                        }
                    }"""
content = content.replace(series_download_button_old, series_download_button_new)

# 4. Update Play Button in Series
series_play_old = """                    Button(
                        onClick = { isDownloadMode = false; showSourceSheet = true },
                        modifier = Modifier.weight(1f).height(50.dp),
                        colors = ButtonDefaults.buttonColors(containerColor = Color(0xFFE50914))
                    ) {
                        Icon(Icons.Default.PlayArrow, contentDescription = "Play", tint = Color.White)
                        Spacer(modifier = Modifier.width(8.dp))
                        Text("Resume", color = Color.White, fontWeight = FontWeight.Bold)
                    }"""

series_play_new = """                    Button(
                        onClick = { 
                            if (downloadItem?.isCompleted == true) {
                                onPlay("local_offline_file://${downloadItem.id}")
                            } else {
                                isDownloadMode = false; showSourceSheet = true 
                            }
                        },
                        modifier = Modifier.weight(1f).height(50.dp),
                        colors = ButtonDefaults.buttonColors(containerColor = Color(0xFFE50914))
                    ) {
                        Icon(Icons.Default.PlayArrow, contentDescription = "Play", tint = Color.White)
                        Spacer(modifier = Modifier.width(8.dp))
                        Text(if (downloadItem?.isCompleted == true) "Resume Offline" else "Resume", color = Color.White, fontWeight = FontWeight.Bold)
                    }"""
content = content.replace(series_play_old, series_play_new)


with open('app/src/main/java/com/example/ui/screens/details/DetailsScreens.kt', 'w') as f:
    f.write(content)

