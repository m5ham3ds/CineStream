import re

with open("app/src/main/java/com/example/ui/screens/home/TrendingScreen.kt", "r") as f:
    content = f.read()

imports = """
import androidx.compose.material3.pulltorefresh.PullToRefreshBox
import androidx.compose.material3.pulltorefresh.rememberPullToRefreshState
"""
if "PullToRefreshBox" not in content:
    content = content.replace("import androidx.compose.material3.*", "import androidx.compose.material3.*\n" + imports)

def add_ptr(match):
    return """
        val ptrState = rememberPullToRefreshState()
        PullToRefreshBox(
            isRefreshing = uiState.isLoading,
            onRefresh = { viewModel.loadData() },
            state = ptrState,
            modifier = Modifier.fillMaxSize()
        ) {
""" + match.group(0)

content = re.sub(
    r'(\s*LazyVerticalGrid\()',
    add_ptr,
    content
)

# the closing brace for PullToRefreshBox
content = content.replace("        }\n    }\n}", "        }\n    }\n}\n}")

with open("app/src/main/java/com/example/ui/screens/home/TrendingScreen.kt", "w") as f:
    f.write(content)

