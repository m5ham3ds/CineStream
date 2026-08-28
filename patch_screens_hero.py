import re
import os

screens = [
    ("app/src/main/java/com/example/ui/screens/home/HomeScreen.kt", "uiState.trendingMovies", "movies = ", "HeroItem(it.id, it.title, it.backdropUrl)", "onMovieClick"),
    ("app/src/main/java/com/example/ui/screens/movies/MoviesScreen.kt", "uiState.movies", "HeroSectionShared", "HeroItem(it.id, it.title, it.backdropUrl)", "onMovieClick"),
    ("app/src/main/java/com/example/ui/screens/series/SeriesScreen.kt", "uiState.series", "HeroSectionShared", "HeroItem(it.id, it.title, it.backdropUrl)", "onSeriesClick"),
    ("app/src/main/java/com/example/ui/screens/anime/AnimeScreen.kt", "uiState.series", "HeroSectionShared", "HeroItem(it.id, it.title, it.backdropUrl)", "onAnimeClick")
]

for file, list_prop, pattern, mapping, click in screens:
    if not os.path.exists(file): continue
    with open(file, "r") as f:
        content = f.read()
    
    if "import com.example.ui.components.HeroCarousel" not in content:
        content = content.replace("import com.example.ui.components.MediaCard", "import com.example.ui.components.MediaCard\nimport com.example.ui.components.HeroCarousel\nimport com.example.ui.components.HeroItem")
        
    if file.endswith("HomeScreen.kt"):
        content = content.replace(
            "HeroCarousel(movies = uiState.trendingMovies.take(5), onClick = onMovieClick)",
            "HeroCarousel(items = uiState.trendingMovies.take(5).map { HeroItem(it.id, it.title, it.backdropUrl) }, onClick = onMovieClick)"
        )
    else:
        # replace HeroSectionShared
        hero_pattern = r"val hero[\w]+ = " + list_prop + r"\.firstOrNull\(\)\n\s*if \(hero[\w]+ != null\) \{\n\s*HeroSectionShared\([\s\S]*?\)\n\s*\}"
        new_hero = f"HeroCarousel(items = {list_prop}.take(5).map {{ HeroItem(it.id, it.title, it.backdropUrl) }}, onClick = {click})"
        content = re.sub(hero_pattern, new_hero, content)
        
    with open(file, "w") as f:
        f.write(content)

