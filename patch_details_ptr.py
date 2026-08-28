import re

def patch_file(filepath, viewmodel_func):
    with open(filepath, "r") as f:
        content = f.read()

    imports = """
import androidx.compose.material3.ExperimentalMaterial3Api
import androidx.compose.material3.pulltorefresh.PullToRefreshBox
import androidx.compose.material3.pulltorefresh.rememberPullToRefreshState
"""
    if "import androidx.compose.material3.pulltorefresh.PullToRefreshBox" not in content:
        content = content.replace("import androidx.compose.material3.*", "import androidx.compose.material3.*\n" + imports)
    
    if filepath == "app/src/main/java/com/example/ui/screens/details/DetailsScreens.kt":
        if "@OptIn(ExperimentalMaterial3Api::class)" not in content:
            content = content.replace("@Composable\nfun MovieDetailsScreen", "@OptIn(ExperimentalMaterial3Api::class)\n@Composable\nfun MovieDetailsScreen")
            content = content.replace("@Composable\nfun SeriesDetailsScreen", "@OptIn(ExperimentalMaterial3Api::class)\n@Composable\nfun SeriesDetailsScreen")
    elif filepath == "app/src/main/java/com/example/ui/screens/details/PersonDetailsScreen.kt":
        if "@OptIn(ExperimentalMaterial3Api::class)" not in content:
            content = content.replace("@Composable\nfun PersonDetailsScreen", "@OptIn(ExperimentalMaterial3Api::class)\n@Composable\nfun PersonDetailsScreen")
    
    if viewmodel_func == "loadMovie(movieId)":
        content = re.sub(
            r'(\s*Column\(\n\s*modifier = Modifier\n\s*\.fillMaxSize\(\)\n\s*\.verticalScroll\(rememberScrollState\(\)\)\n\s*\) \{)',
            r"""
            val ptrState = rememberPullToRefreshState()
            PullToRefreshBox(
                isRefreshing = uiState.isLoading,
                onRefresh = { viewModel.""" + viewmodel_func + r""" },
                state = ptrState,
                modifier = Modifier.fillMaxSize().padding(padding)
            ) {\1""",
            content,
            count=1 # only the first one
        )
    elif viewmodel_func == "loadSeries(seriesId)":
        # in SeriesDetailsScreen
        content = re.sub(
            r'(\s*Column\(\n\s*modifier = Modifier\n\s*\.fillMaxSize\(\)\n\s*\.verticalScroll\(rememberScrollState\(\)\)\n\s*\) \{)',
            r"""
            val ptrState = rememberPullToRefreshState()
            PullToRefreshBox(
                isRefreshing = uiState.isLoading,
                onRefresh = { viewModel.""" + viewmodel_func + r""" },
                state = ptrState,
                modifier = Modifier.fillMaxSize().padding(padding)
            ) {\1""",
            content
        )
    elif viewmodel_func == "loadPerson(personId)":
        content = re.sub(
            r'(\s*Column\(\n\s*modifier = Modifier\n\s*\.fillMaxSize\(\)\n\s*\.verticalScroll\(rememberScrollState\(\)\)\n\s*\) \{)',
            r"""
            val ptrState = rememberPullToRefreshState()
            PullToRefreshBox(
                isRefreshing = uiState.isLoading,
                onRefresh = { viewModel.""" + viewmodel_func + r""" },
                state = ptrState,
                modifier = Modifier.fillMaxSize().padding(padding)
            ) {\1""",
            content
        )
        
    with open(filepath, "w") as f:
        f.write(content)

patch_file("app/src/main/java/com/example/ui/screens/details/DetailsScreens.kt", "loadMovie(movieId)")
patch_file("app/src/main/java/com/example/ui/screens/details/DetailsScreens.kt", "loadSeries(seriesId)")
patch_file("app/src/main/java/com/example/ui/screens/details/PersonDetailsScreen.kt", "loadPerson(personId)")

