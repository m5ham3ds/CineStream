import re

with open("app/src/main/java/com/example/ui/screens/movies/MoviesScreen.kt", "r") as f:
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
        onRefresh = { viewModel.loadMovies() },
        state = ptrState,
        modifier = Modifier.fillMaxSize()
    ) {
"""

content = re.sub(
    r'(    val categories = listOf\(\n\s*CategoryItem\("Movies", Icons\.Default\.LocalMovies\),\n\s*CategoryItem\("Genres", Icons\.Default\.Category\),\n\s*CategoryItem\("New Releases", Icons\.Default\.NewReleases\),\n\s*CategoryItem\("Top Rated", Icons\.Default\.Star\)\n\s*\))',
    add_ptr,
    content
)

# And we need to add the closing brace at the very end.
content = content.replace(
    "        if (showBottomSheet) {\n            MediaActionBottomSheet(",
    "    }\n        if (showBottomSheet) {\n            MediaActionBottomSheet("
)

# Also add @OptIn(ExperimentalMaterial3Api::class) to MoviesScreen
if "@OptIn(ExperimentalMaterial3Api::class)" not in content:
    content = content.replace("@Composable\nfun MoviesScreen", "@OptIn(ExperimentalMaterial3Api::class)\n@Composable\nfun MoviesScreen")

with open("app/src/main/java/com/example/ui/screens/movies/MoviesScreen.kt", "w") as f:
    f.write(content)

