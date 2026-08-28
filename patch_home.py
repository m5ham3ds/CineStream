import re

with open("app/src/main/java/com/example/ui/screens/home/HomeScreen.kt", "r") as f:
    content = f.read()

# Add HistoryRepository and HistoryItem imports
imports = """
import androidx.compose.ui.platform.LocalContext
import com.example.data.repository.HistoryRepository
import androidx.compose.runtime.collectAsState
"""
content = content.replace("import com.example.ui.components.MediaCard", imports + "\nimport com.example.ui.components.MediaCard\nimport com.example.ui.components.ContinueWatchingCardShared")

# Add HistoryRepository instance
state_def = """
    val uiState by viewModel.uiState.collectAsState()
    val context = LocalContext.current
    val historyRepository = remember { HistoryRepository(context) }
    val historyItems by historyRepository.getHistoryItems().collectAsState(initial = emptyList())
"""
content = content.replace("val uiState by viewModel.uiState.collectAsState()", state_def.strip())

# Replace the Continue Watching section
old_continue = r'// Continue Watching \(Demo Item\)\s*SectionTitle\("Continue Watching", onSeeAllClick = onNavigateToWatching\)\s*ContinueWatchingCard\(\)\s*Spacer\(modifier = Modifier\.height\(24\.dp\)\)'
new_continue = """
        // Continue Watching
        if (historyItems.isNotEmpty()) {
            SectionTitle("متابعة المشاهدة", onSeeAllClick = onNavigateToWatching)
            LazyRow(
                contentPadding = PaddingValues(horizontal = 16.dp),
                horizontalArrangement = Arrangement.spacedBy(16.dp)
            ) {
                items(historyItems) { item ->
                    ContinueWatchingCardShared(item = item) {
                        if (item.isMovie) onMovieClick(item.id) else onSeriesClick(item.id)
                    }
                }
            }
            Spacer(modifier = Modifier.height(24.dp))
        }
"""
content = re.sub(old_continue, new_continue.strip(), content)

# Remove the ContinueWatchingCard definition at the bottom
content = re.sub(r'@Composable\nfun ContinueWatchingCard\(\).*?\}\s*\}\s*\}', "", content, flags=re.DOTALL)

with open("app/src/main/java/com/example/ui/screens/home/HomeScreen.kt", "w") as f:
    f.write(content)
