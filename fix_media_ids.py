import os
import re

files = [
    "app/src/main/java/com/example/ui/screens/anime/AnimeScreen.kt",
    "app/src/main/java/com/example/ui/screens/library/LibraryScreen.kt",
    "app/src/main/java/com/example/ui/screens/series/SeriesScreen.kt",
    "app/src/main/java/com/example/ui/screens/home/HomeScreen.kt",
    "app/src/main/java/com/example/ui/screens/home/TrendingScreen.kt",
    "app/src/main/java/com/example/ui/screens/home/NewReleasesScreen.kt",
    "app/src/main/java/com/example/ui/screens/home/PopularScreen.kt",
    "app/src/main/java/com/example/ui/screens/search/SearchScreen.kt",
    "app/src/main/java/com/example/ui/screens/movies/MoviesScreen.kt"
]

for f in files:
    with open(f, "r") as file:
        content = file.read()
    
    # Remove duplicate mediaId = ...
    content = re.sub(r'(mediaId\s*=\s*[a-zA-Z0-9_\.]+,(\s*)){2,}', r'\1', content)
    
    with open(f, "w") as file:
        file.write(content)
