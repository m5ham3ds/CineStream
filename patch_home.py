import re

with open("app/src/main/java/com/example/ui/screens/home/HomeScreen.kt", "r") as f:
    content = f.read()

# Update signature
old_sig = """fun HomeScreen(
    onMovieClick: (String) -> Unit,
    onSeriesClick: (String) -> Unit,
    onNavigateToTrending: () -> Unit = {},
    onNavigateToWatching: () -> Unit = {},
    viewModel: HomeViewModel = viewModel(factory = ViewModelFactory())
)"""
new_sig = """fun HomeScreen(
    onMovieClick: (String) -> Unit,
    onSeriesClick: (String) -> Unit,
    onNavigateToTrending: () -> Unit = {},
    onNavigateToWatching: () -> Unit = {},
    onNavigateToPopular: () -> Unit = {},
    onNavigateToNewReleases: () -> Unit = {},
    viewModel: HomeViewModel = viewModel(factory = ViewModelFactory())
)"""
content = content.replace(old_sig, new_sig)

# Add see all clicks
content = content.replace('SectionTitleShared("Trending Now")', 'SectionTitleShared("Trending Now", onSeeAllClick = onNavigateToTrending)')
content = content.replace('SectionTitleShared("Continue Watching")', 'SectionTitleShared("Continue Watching", onSeeAllClick = onNavigateToWatching)')
content = content.replace('SectionTitleShared("Popular Movies")', 'SectionTitleShared("Popular Movies", onSeeAllClick = onNavigateToPopular)')
content = content.replace('SectionTitleShared("Popular Series")', 'SectionTitleShared("Popular Series", onSeeAllClick = onNavigateToPopular)')
content = content.replace('SectionTitleShared("New Releases")', 'SectionTitleShared("New Releases", onSeeAllClick = onNavigateToNewReleases)')

with open("app/src/main/java/com/example/ui/screens/home/HomeScreen.kt", "w") as f:
    f.write(content)
