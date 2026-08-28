import re

with open("app/src/main/java/com/example/ui/components/SharedUI.kt", "r") as f:
    content = f.read()

# Add import for HistoryItem
content = content.replace("import com.example.domain.models.Series", "import com.example.domain.models.Series\nimport com.example.data.model.HistoryItem")

# Replace ContinueWatchingCardShared
old_card = r'@Composable\nfun ContinueWatchingCardShared\(\).*?\}\s*\}\s*\}'
new_card = """@Composable
fun ContinueWatchingCardShared(item: HistoryItem, onClick: () -> Unit) {
    Box(
        modifier = Modifier
            .width(260.dp)
            .clip(RoundedCornerShape(12.dp))
            .background(Color(0xFF1E1E20))
            .clickable { onClick() }
    ) {
        Row(
            modifier = Modifier.fillMaxWidth(),
            verticalAlignment = Alignment.CenterVertically
        ) {
            Box(modifier = Modifier.width(100.dp).height(70.dp)) {
                AsyncImage(
                    model = item.posterUrl,
                    contentDescription = item.title,
                    contentScale = ContentScale.Crop,
                    modifier = Modifier.fillMaxSize()
                )
                Box(modifier = Modifier.align(Alignment.BottomStart).fillMaxWidth().height(3.dp).background(Color.DarkGray)) {
                    Box(modifier = Modifier.fillMaxWidth(0.5f).height(3.dp).background(Color(0xFFE50914)))
                }
            }
            
            Column(
                modifier = Modifier
                    .weight(1f)
                    .padding(horizontal = 12.dp)
            ) {
                Text(item.title, color = Color.White, fontWeight = FontWeight.SemiBold, fontSize = 14.sp, maxLines = 1)
                Spacer(modifier = Modifier.height(4.dp))
                Text(if (item.isMovie) "فيلم" else "مسلسل", color = Color.Gray, fontSize = 12.sp)
            }
        }
    }
}
"""

content = re.sub(old_card, new_card.strip(), content, flags=re.DOTALL)

with open("app/src/main/java/com/example/ui/components/SharedUI.kt", "w") as f:
    f.write(content)

