import re

for filepath in ["app/src/main/java/com/example/ui/screens/details/DetailsScreens.kt", "app/src/main/java/com/example/ui/screens/details/PersonDetailsScreen.kt"]:
    with open(filepath, "r") as f:
        content = f.read()

    # Find all PullToRefreshBox blocks and remove them entirely.
    # Wait, we want to replace them with just the `Column(` part.
    
    # Let's match the block we inserted:
    #             val ptrState = rememberPullToRefreshState()
    #             PullToRefreshBox(
    #                 isRefreshing = uiState.isLoading,
    #                 onRefresh = { viewModel.loadMovie(movieId) },
    #                 state = ptrState,
    #                 modifier = Modifier.fillMaxSize().padding(padding)
    #             ) {
    # It might be repeated.
    
    content = re.sub(
        r'\s*val ptrState = rememberPullToRefreshState\(\)\n\s*PullToRefreshBox\(\n\s*isRefreshing = uiState\.isLoading,\n\s*onRefresh = \{ viewModel\.[^\}]+\},\n\s*state = ptrState,\n\s*modifier = Modifier\.fillMaxSize\(\)\.padding\(padding\)\n\s*\) \{',
        '',
        content
    )
    
    # We also did it for PersonDetailsScreen?
    content = re.sub(
        r'\s*val ptrState = rememberPullToRefreshState\(\)\n\s*PullToRefreshBox\(\n\s*isRefreshing = uiState\.isLoading,\n\s*onRefresh = \{ viewModel\.[^\}]+\},\n\s*state = ptrState,\n\s*modifier = Modifier\.fillMaxSize\(\)\.padding\(padding\)\n\s*\) \{',
        '',
        content
    )

    with open(filepath, "w") as f:
        f.write(content)
