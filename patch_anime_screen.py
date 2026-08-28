import re

with open("app/src/main/java/com/example/ui/screens/anime/AnimeScreen.kt", "r") as f:
    content = f.read()

imports = """
import androidx.compose.foundation.lazy.grid.GridItemSpan
import androidx.compose.foundation.lazy.LazyRow
import androidx.compose.foundation.lazy.items as lazyRowItems
import androidx.compose.ui.platform.LocalContext
import com.example.data.repository.HistoryRepository
import com.example.ui.components.SectionTitleShared
import com.example.ui.components.ContinueWatchingCardShared
"""
content = content.replace("import com.example.ui.components.MediaCard", imports + "\nimport com.example.ui.components.MediaCard")

history_state = """
    val uiState by viewModel.uiState.collectAsState()
    val context = LocalContext.current
    val historyRepository = remember { HistoryRepository(context) }
    val historyItems by historyRepository.getHistoryItems().collectAsState(initial = emptyList())
    // For anime, we assume it's series for now
    val animeHistory = historyItems.filter { !it.isMovie } 
"""
content = content.replace("val uiState by viewModel.uiState.collectAsState()", history_state.strip())

grid_content = """
            LazyVerticalGrid(
                columns = GridCells.Fixed(3),
                contentPadding = PaddingValues(16.dp),
                horizontalArrangement = Arrangement.spacedBy(16.dp),
                verticalArrangement = Arrangement.spacedBy(16.dp),
                modifier = Modifier.fillMaxSize()
            ) {
                if (animeHistory.isNotEmpty()) {
                    item(span = { GridItemSpan(maxLineSpan) }) {
                        Column {
                            SectionTitleShared("متابعة المشاهدة")
                            LazyRow(
                                contentPadding = PaddingValues(horizontal = 0.dp),
                                horizontalArrangement = Arrangement.spacedBy(16.dp)
                            ) {
                                lazyRowItems(animeHistory) { item ->
                                    ContinueWatchingCardShared(item = item) {
                                        onAnimeClick(item.id)
                                    }
                                }
                            }
                            Spacer(modifier = Modifier.height(16.dp))
                            SectionTitleShared("الأنمي")
                        }
                    }
                }
                
                items(uiState.series) { series ->
"""
content = re.sub(r'LazyVerticalGrid\(.*?\{.*?items\(uiState\.series\) \{ series ->', grid_content.strip(), content, flags=re.DOTALL)

with open("app/src/main/java/com/example/ui/screens/anime/AnimeScreen.kt", "w") as f:
    f.write(content)

