import re

def update_screen(file_path, is_movie=True):
    with open(file_path, "r") as f:
        content = f.read()

    # 1. Update Signature
    if is_movie:
        old_sig = """fun MoviesScreen(
    onMovieClick: (String) -> Unit,
    viewModel: MoviesViewModel = viewModel(factory = ViewModelFactory())
)"""
        new_sig = """fun MoviesScreen(
    onMovieClick: (String) -> Unit,
    onNavigateToTrending: () -> Unit = {},
    onNavigateToWatching: () -> Unit = {},
    onNavigateToPopular: () -> Unit = {},
    onNavigateToNewReleases: () -> Unit = {},
    viewModel: MoviesViewModel = viewModel(factory = ViewModelFactory())
)"""
        content = content.replace(old_sig, new_sig)
    else:
        old_sig = """fun SeriesScreen(
    onSeriesClick: (String) -> Unit,
    viewModel: SeriesViewModel = viewModel(factory = ViewModelFactory())
)"""
        new_sig = """fun SeriesScreen(
    onSeriesClick: (String) -> Unit,
    onNavigateToTrending: () -> Unit = {},
    onNavigateToWatching: () -> Unit = {},
    onNavigateToPopular: () -> Unit = {},
    onNavigateToNewReleases: () -> Unit = {},
    viewModel: SeriesViewModel = viewModel(factory = ViewModelFactory())
)"""
        content = content.replace(old_sig, new_sig)

    # 2. Swap Hero Section and Categories
    # We will just find them and swap.
    categories_pattern = r"(        // Categories Tab Row.*?)(        // Hero Section.*?)(        Spacer\(modifier = Modifier.height\(24.dp\)\))"
    
    match = re.search(categories_pattern, content, flags=re.DOTALL)
    if match:
        categories = match.group(1)
        hero = match.group(2)
        spacer = match.group(3)
        # Add a spacer between hero and categories if we swap
        new_order = hero + "\n        Spacer(modifier = Modifier.height(16.dp))\n" + categories + "\n" + spacer
        content = content.replace(match.group(0), new_order)
    
    # 3. Add See All callbacks
    content = content.replace('SectionTitleShared("Continue Watching")', 'SectionTitleShared("Continue Watching", onSeeAllClick = onNavigateToWatching)')
    
    if is_movie:
        content = content.replace('SectionTitleShared("Popular Movies")', 'SectionTitleShared("Popular Movies", onSeeAllClick = onNavigateToPopular)')
    else:
        content = content.replace('SectionTitleShared("Popular Series")', 'SectionTitleShared("Popular Series", onSeeAllClick = onNavigateToPopular)')
        
    content = content.replace('SectionTitleShared("New Releases")', 'SectionTitleShared("New Releases", onSeeAllClick = onNavigateToNewReleases)')

    with open(file_path, "w") as f:
        f.write(content)

update_screen("app/src/main/java/com/example/ui/screens/movies/MoviesScreen.kt", is_movie=True)
update_screen("app/src/main/java/com/example/ui/screens/series/SeriesScreen.kt", is_movie=False)

