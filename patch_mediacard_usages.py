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
    
    # We want to replace `onClick = { ... }` with `mediaId = XXX,\n                    onClick = { ... }`
    # Or just `isMovie = isMovie,` -> `isMovie = isMovie, mediaId = id,`
    # We have to be careful since they use different variable names (e.g. `series.id`, `movie.id`, `id`, `item.id`).
    
    # In LibraryScreen.kt: item.id
    content = content.replace("onClick = { onItemClick(item.id, item.isMovie) }", "mediaId = item.id,\n                        onClick = { onItemClick(item.id, item.isMovie) }")
    
    # In AnimeScreen: series.id
    content = content.replace("onClick = { onAnimeClick(series.id) }", "mediaId = series.id,\n                        onClick = { onAnimeClick(series.id) }")
    
    # In SeriesScreen: series.id
    content = content.replace("onClick = { onSeriesClick(series.id) }", "mediaId = series.id,\n                        onClick = { onSeriesClick(series.id) }")
    
    # In MoviesScreen: movie.id
    content = content.replace("onClick = { onMovieClick(movie.id) }", "mediaId = movie.id,\n                        onClick = { onMovieClick(movie.id) }")
    
    # In HomeScreen: movie.id, series.id
    content = content.replace("onClick = { onMovieClick(movie.id) }", "mediaId = movie.id,\n                    onClick = { onMovieClick(movie.id) }")
    content = content.replace("onClick = { onSeriesClick(series.id) }", "mediaId = series.id,\n                    onClick = { onSeriesClick(series.id) }")
    content = content.replace("onClick = { onAnimeClick(anime.id) }", "mediaId = anime.id,\n                    onClick = { onAnimeClick(anime.id) }")

    # In SearchScreen:
    content = content.replace("onClick = { onMovieClick(movie.id) }", "mediaId = movie.id,\n                            onClick = { onMovieClick(movie.id) }")
    content = content.replace("onClick = { onSeriesClick(series.id) }", "mediaId = series.id,\n                            onClick = { onSeriesClick(series.id) }")

    # In TrendingScreen, PopularScreen, NewReleasesScreen: id
    content = content.replace("onClick = { onItemClick(id, isMovie) }", "mediaId = id,\n                    onClick = { onItemClick(id, isMovie) }")
    
    with open(f, "w") as file:
        file.write(content)

