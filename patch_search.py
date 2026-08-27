import re

with open("app/src/main/java/com/example/ui/screens/search/SearchScreen.kt", "r") as f:
    content = f.read()

old_sig = """fun SearchScreen(
    onMediaClick: (String, Boolean) -> Unit,
    viewModel: SearchViewModel = viewModel(factory = ViewModelFactory())
)"""

new_sig = """fun SearchScreen(
    onMediaClick: (String, Boolean) -> Unit,
    onNavigateToTrending: () -> Unit = {},
    viewModel: SearchViewModel = viewModel(factory = ViewModelFactory())
)"""

content = content.replace(old_sig, new_sig)
content = content.replace('SectionTitleShared("Trending Now")', 'SectionTitleShared("Trending Now", onSeeAllClick = onNavigateToTrending)')

with open("app/src/main/java/com/example/ui/screens/search/SearchScreen.kt", "w") as f:
    f.write(content)

