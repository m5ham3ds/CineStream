import os
import re

screens = {
    "app/src/main/java/com/example/ui/screens/home/HomeScreen.kt": "HeroItem(it.id, it.title, it.backdropUrl, true)",
    "app/src/main/java/com/example/ui/screens/movies/MoviesScreen.kt": "HeroItem(it.id, it.title, it.backdropUrl, true)",
    "app/src/main/java/com/example/ui/screens/series/SeriesScreen.kt": "HeroItem(it.id, it.title, it.backdropUrl, false)",
    "app/src/main/java/com/example/ui/screens/anime/AnimeScreen.kt": "HeroItem(it.id, it.title, it.backdropUrl, false)"
}

for file, replacement in screens.items():
    if not os.path.exists(file): continue
    with open(file, "r") as f:
        content = f.read()
    content = content.replace("HeroItem(it.id, it.title, it.backdropUrl)", replacement)
    with open(file, "w") as f:
        f.write(content)

with open("app/src/main/java/com/example/ui/components/HeroCarousel.kt", "r") as f:
    hero_content = f.read()

hero_content = hero_content.replace(
    "data class HeroItem(val id: String, val title: String, val backdropUrl: String)",
    "data class HeroItem(val id: String, val title: String, val backdropUrl: String, val isMovie: Boolean = true)"
)

with open("app/src/main/java/com/example/ui/components/HeroCarousel.kt", "w") as f:
    f.write(hero_content)
