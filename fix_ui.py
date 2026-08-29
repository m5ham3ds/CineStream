import re

with open('app/src/main/java/com/example/ui/screens/downloads/DownloadsScreen.kt', 'r') as f:
    content = f.read()

replacement = """        Column(modifier = Modifier.weight(1f)) {
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
        }"""

pattern = r'        Column\(modifier = Modifier\.weight\(1f\)\) \{.*?Text\(if \(item\.isCompleted\) "Completed".*?\}\n        \}'

content = re.sub(pattern, replacement, content, flags=re.DOTALL)

with open('app/src/main/java/com/example/ui/screens/downloads/DownloadsScreen.kt', 'w') as f:
    f.write(content)
