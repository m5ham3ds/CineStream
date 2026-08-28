import re

with open("app/src/main/java/com/example/ui/screens/series/SeriesScreen.kt", "r") as f:
    content = f.read()

imports = """
import androidx.compose.material3.ExperimentalMaterial3Api
import androidx.compose.material3.pulltorefresh.PullToRefreshBox
import androidx.compose.material3.pulltorefresh.rememberPullToRefreshState
"""

if "import androidx.compose.material3.pulltorefresh.PullToRefreshBox" not in content:
    content = content.replace("import androidx.compose.material3.*", "import androidx.compose.material3.*\n" + imports)

def add_ptr(match):
    prefix = match.group(1) 
    return prefix + """
    val ptrState = rememberPullToRefreshState()
    
    PullToRefreshBox(
        isRefreshing = uiState.isLoading,
        onRefresh = { viewModel.loadSeries() },
        state = ptrState,
        modifier = Modifier.fillMaxSize()
    ) {
"""

content = re.sub(
    r'(    val categories = listOf\("All", "Trending", "New Releases", "Top Rated", "Genres"\))',
    add_ptr,
    content
)

# And we need to add the closing brace at the very end.
content = content.replace(
    "        if (showBottomSheet) {\n            MediaActionBottomSheet(",
    "    }\n        if (showBottomSheet) {\n            MediaActionBottomSheet("
)

# Also add @OptIn(ExperimentalMaterial3Api::class) to SeriesScreen
if "@OptIn(ExperimentalMaterial3Api::class)" not in content:
    content = content.replace("@Composable\nfun SeriesScreen", "@OptIn(ExperimentalMaterial3Api::class)\n@Composable\nfun SeriesScreen")

with open("app/src/main/java/com/example/ui/screens/series/SeriesScreen.kt", "w") as f:
    f.write(content)

