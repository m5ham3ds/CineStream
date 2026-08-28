import re
import os

files = [
    "app/src/main/java/com/example/ui/screens/home/TrendingScreen.kt",
    "app/src/main/java/com/example/ui/screens/home/PopularScreen.kt",
    "app/src/main/java/com/example/ui/screens/home/NewReleasesScreen.kt",
    "app/src/main/java/com/example/ui/screens/home/UpcomingScreen.kt"
]

target_code = """        PullToRefreshBox(isRefreshing = uiState.isLoading, onRefresh = { viewModel.loadData() }, state = ptrState, modifier = Modifier.fillMaxSize()) {
            LazyVerticalGrid(columns = GridCells.Fixed(3)"""
            
new_code = """        PullToRefreshBox(isRefreshing = uiState.isLoading, onRefresh = { viewModel.loadData() }, state = ptrState, modifier = Modifier.fillMaxSize()) {
            if (uiState.isLoading && items.isEmpty()) {
                com.example.ui.components.GridScreenSkeleton()
            } else {
                LazyVerticalGrid(columns = GridCells.Fixed(3)"""

for file in files:
    if not os.path.exists(file): continue
    with open(file, "r") as f:
        content = f.read()

    # Need to close the else block
    content = content.replace(target_code, new_code)
    # The LazyVerticalGrid block needs a closing brace for the else.
    # It ends with:
    #             }
    #         }
    #     }
    # }
    
    # Actually, simpler way is to just do it precisely
    
    with open(file, "w") as f:
        f.write(content)

