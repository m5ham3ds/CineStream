import re

with open('app/src/main/java/com/example/ui/screens/downloads/DownloadsScreen.kt', 'r') as f:
    content = f.read()

# We need to find the part where it got ruined and replace it with the correct original "Download More Card" and then my new "DownloadItemRow".
# The ruined part starts exactly at line 254:
# Column(modifier = Modifier.weight(1f)) {
#             Text(item.title, color = Color.White, fontWeight = FontWeight.Bold, maxLines = 1, overflow = TextOverflow.Ellipsis)

bad_part = r'Column\(modifier = Modifier\.weight\(1f\)\) \{\s*Text\(item\.title, color = Color\.White, fontWeight = FontWeight\.Bold, maxLines = 1, overflow = TextOverflow\.Ellipsis\).*?fun DownloadStat'

replacement = """Column(modifier = Modifier.weight(1f)) {
                        Text("Download more content", color = Color.White, fontSize = 16.sp, fontWeight = FontWeight.Bold)
                        Spacer(modifier = Modifier.height(4.dp))
                        Text("Find movies and series to download and watch offline.", color = Color.Gray, fontSize = 12.sp, lineHeight = 16.sp)
                        Spacer(modifier = Modifier.height(12.dp))
                        Button(
                            onClick = onNavigateToHome,
                            colors = ButtonDefaults.buttonColors(containerColor = Color(0xFF4A1010)),
                            shape = RoundedCornerShape(percent = 50),
                            contentPadding = PaddingValues(horizontal = 16.dp, vertical = 0.dp),
                            modifier = Modifier.height(36.dp)
                        ) {
                            Text("Browse Content", color = Color.White, fontSize = 12.sp, fontWeight = FontWeight.SemiBold)
                        }
                    }
                }
            }
        }
    }
}

@Composable
fun DownloadItemRow(item: DownloadItem, onClick: () -> Unit, onPauseResume: () -> Unit, onDelete: () -> Unit) {
    Row(
        modifier = Modifier
            .fillMaxWidth()
            .clip(RoundedCornerShape(12.dp))
            .background(Color(0xFF161618))
            .clickable { onClick() }
            .padding(12.dp),
        verticalAlignment = Alignment.CenterVertically
    ) {
        AsyncImage(
            model = item.posterUrl,
            contentDescription = item.title,
            contentScale = ContentScale.Crop,
            modifier = Modifier
                .width(60.dp)
                .aspectRatio(3f / 4f)
                .clip(RoundedCornerShape(8.dp))
        )
        Spacer(modifier = Modifier.width(16.dp))
        Column(modifier = Modifier.weight(1f)) {
            Text(item.title, color = Color.White, fontWeight = FontWeight.Bold, maxLines = 1, overflow = TextOverflow.Ellipsis)
            Spacer(modifier = Modifier.height(4.dp))
            Row(horizontalArrangement = Arrangement.SpaceBetween, modifier = Modifier.fillMaxWidth()) {
                Text(if (item.isMovie) "Movie" else "Series", color = Color.Gray, fontSize = 12.sp)
                Text("${(item.progress * 100).toInt()}%", color = Color.Gray, fontSize = 12.sp)
            }
            Spacer(modifier = Modifier.height(8.dp))
            LinearProgressIndicator(
                progress = { item.progress },
                modifier = Modifier.fillMaxWidth().height(4.dp).clip(RoundedCornerShape(2.dp)),
                color = if (item.isCompleted) Color.Green else Color(0xFFE50914),
                trackColor = Color(0xFF2A2A2E)
            )
            Spacer(modifier = Modifier.height(8.dp))
            Row(verticalAlignment = Alignment.CenterVertically) {
                Text(if (item.isCompleted) "Completed" else if (item.isPaused) "Paused" else "Downloading...", color = if (item.isCompleted) Color.Green else if (item.isPaused) Color.Yellow else Color(0xFFE50914), fontSize = 12.sp)
            }
        }
        Spacer(modifier = Modifier.width(8.dp))
        if (!item.isCompleted) {
            IconButton(onClick = onPauseResume) {
                Icon(if (item.isPaused) Icons.Default.PlayArrow else Icons.Default.Pause, contentDescription = "Pause/Resume", tint = Color.White)
            }
        }
        IconButton(onClick = onDelete) {
            Icon(Icons.Default.Close, contentDescription = "Delete", tint = Color.Gray)
        }
    }
}

@Composable
fun DownloadStat"""

content = re.sub(bad_part, replacement, content, flags=re.DOTALL)

with open('app/src/main/java/com/example/ui/screens/downloads/DownloadsScreen.kt', 'w') as f:
    f.write(content)
