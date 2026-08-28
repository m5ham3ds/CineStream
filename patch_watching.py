import re

with open("app/src/main/java/com/example/ui/screens/home/WatchingScreen.kt", "r") as f:
    content = f.read()

imports = """
import androidx.compose.ui.platform.LocalContext
import androidx.compose.runtime.collectAsState
import androidx.compose.runtime.getValue
import androidx.compose.runtime.remember
import androidx.compose.foundation.lazy.items
import com.example.data.repository.HistoryRepository
import com.example.data.model.HistoryItem
"""
content = content.replace("import coil.compose.AsyncImage", imports + "\nimport coil.compose.AsyncImage")

# Replace screen
new_screen = """
@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun WatchingScreen(
    onItemClick: (String, Boolean) -> Unit,
    onBack: () -> Unit
) {
    val context = LocalContext.current
    val historyRepository = remember { HistoryRepository(context) }
    val historyItems by historyRepository.getHistoryItems().collectAsState(initial = emptyList())

    Column(modifier = Modifier.fillMaxSize().background(Color.Black)) {
        CenterAlignedTopAppBar(
            title = {
                Column(horizontalAlignment = Alignment.CenterHorizontally) {
                    Text("متابعة المشاهدة", color = Color.White, fontWeight = FontWeight.Bold, fontSize = 20.sp)
                }
            },
            navigationIcon = {
                IconButton(onClick = onBack) {
                    Icon(Icons.AutoMirrored.Filled.ArrowBack, contentDescription = "Back", tint = Color.White)
                }
            },
            colors = TopAppBarDefaults.centerAlignedTopAppBarColors(containerColor = Color.Black)
        )
        
        if (historyItems.isEmpty()) {
            Box(modifier = Modifier.fillMaxSize(), contentAlignment = Alignment.Center) {
                Text("لا توجد عناصر للمتابعة", color = Color.Gray, fontSize = 16.sp)
            }
        } else {
            LazyColumn(
                contentPadding = PaddingValues(start = 16.dp, end = 16.dp, top = 8.dp, bottom = 100.dp),
                verticalArrangement = Arrangement.spacedBy(16.dp),
                modifier = Modifier.fillMaxSize()
            ) {
                items(historyItems) { item ->
                    DetailedContinueWatchingCard(item = item, onClick = { onItemClick(item.id, item.isMovie) })
                }
            }
        }
    }
}
"""
content = re.sub(r'@OptIn\(ExperimentalMaterial3Api::class\)\n@Composable\nfun WatchingScreen.*?\}\n\}\n\n', new_screen.strip() + "\n\n", content, flags=re.DOTALL)

# Delete DetailedWatchingItem
content = re.sub(r'data class DetailedWatchingItem.*?\)\n', '', content, flags=re.DOTALL)

# Modify DetailedContinueWatchingCard
old_card = r'@Composable\nfun DetailedContinueWatchingCard.*?\}'
new_card = """
@Composable
fun DetailedContinueWatchingCard(item: HistoryItem, onClick: () -> Unit) {
    Row(
        modifier = Modifier
            .fillMaxWidth()
            .height(100.dp)
            .clip(RoundedCornerShape(12.dp))
            .background(Color(0xFF161618))
            .clickable { onClick() },
        verticalAlignment = Alignment.CenterVertically
    ) {
        Box(
            modifier = Modifier
                .width(140.dp)
                .fillMaxHeight()
        ) {
            AsyncImage(
                model = item.posterUrl,
                contentDescription = item.title,
                contentScale = ContentScale.Crop,
                modifier = Modifier.fillMaxSize()
            )
            
            // Progress Bar
            Box(
                modifier = Modifier
                    .fillMaxWidth()
                    .height(4.dp)
                    .align(Alignment.BottomStart)
                    .background(Color.White.copy(alpha = 0.3f))
            ) {
                Box(
                    modifier = Modifier
                        .fillMaxWidth(0.5f)
                        .fillMaxHeight()
                        .background(Color(0xFFE50914))
                )
            }
        }
        
        Column(
            modifier = Modifier
                .weight(1f)
                .padding(horizontal = 16.dp, vertical = 8.dp),
            verticalArrangement = Arrangement.SpaceBetween
        ) {
            Column {
                Text(
                    text = item.title,
                    color = Color.White,
                    fontWeight = FontWeight.Bold,
                    fontSize = 14.sp,
                    maxLines = 1
                )
                Spacer(modifier = Modifier.height(2.dp))
                Text(if (item.isMovie) "فيلم" else "مسلسل", color = Color.Gray, fontSize = 12.sp)
            }
            
            Row(
                modifier = Modifier.fillMaxWidth(),
                horizontalArrangement = Arrangement.End,
                verticalAlignment = Alignment.CenterVertically
            ) {
                Box(
                    modifier = Modifier
                        .size(32.dp)
                        .clip(CircleShape)
                        .background(Color(0xFF2A2A2E)),
                    contentAlignment = Alignment.Center
                ) {
                    Icon(Icons.Default.PlayArrow, contentDescription = "Play", tint = Color(0xFFE50914), modifier = Modifier.size(16.dp))
                }
                Spacer(modifier = Modifier.width(12.dp))
                Icon(Icons.Default.MoreVert, contentDescription = "More", tint = Color.Gray, modifier = Modifier.size(20.dp))
            }
        }
    }
}
"""
content = re.sub(old_card, new_card.strip(), content, flags=re.DOTALL)

with open("app/src/main/java/com/example/ui/screens/home/WatchingScreen.kt", "w") as f:
    f.write(content)

