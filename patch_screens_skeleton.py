import re
import os

files = [
    "app/src/main/java/com/example/ui/screens/home/HomeScreen.kt",
    "app/src/main/java/com/example/ui/screens/movies/MoviesScreen.kt",
    "app/src/main/java/com/example/ui/screens/series/SeriesScreen.kt",
    "app/src/main/java/com/example/ui/screens/anime/AnimeScreen.kt"
]

target_code = """    if (uiState.isLoading) {
        Box(modifier = Modifier.fillMaxSize(), contentAlignment = Alignment.Center) {
            CircularProgressIndicator(color = Color(0xFFE50914))
        }
        return
    }"""
    
new_code = """    if (uiState.isLoading) {
        MediaScreenSkeleton()
        return
    }"""

target_code_2 = """        if (uiState.isLoading && uiState.trendingMovies.isEmpty()) {
            Box(modifier = Modifier.fillMaxSize(), contentAlignment = Alignment.Center) {
                CircularProgressIndicator(color = Color(0xFFE50914))
            }
        }"""
        
new_code_2 = """        if (uiState.isLoading && uiState.trendingMovies.isEmpty()) {
            MediaScreenSkeleton()
        }"""

for file in files:
    if not os.path.exists(file): continue
    with open(file, "r") as f:
        content = f.read()

    content = content.replace(target_code, new_code)
    content = content.replace(target_code_2, new_code_2)

    with open(file, "w") as f:
        f.write(content)

