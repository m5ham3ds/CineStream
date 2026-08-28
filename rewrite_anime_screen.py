import re

with open("app/src/main/java/com/example/ui/screens/movies/MoviesScreen.kt", "r") as f:
    content = f.read()

content = content.replace("package com.example.ui.screens.movies", "package com.example.ui.screens.anime")
content = content.replace("MoviesScreen", "AnimeScreen")
content = content.replace("MoviesViewModel", "AnimeViewModel")
content = content.replace("onMovieClick", "onAnimeClick")
content = content.replace("loadMovies", "loadData")
content = content.replace("uiState.movies", "uiState.series")
content = content.replace("movieHistoryItems", "animeHistoryItems")
content = content.replace("val animeHistoryItems = historyItems.filter { it.isMovie }", "val animeHistoryItems = historyItems.filter { !it.isMovie }") # Assume anime is not movie for history
content = content.replace("movie.title", "series.title")
content = content.replace("movie.posterUrl", "series.posterUrl")
content = content.replace("movie.id", "series.id")
content = content.replace("movie ->", "series ->")
content = content.replace("heroMovie", "heroSeries")
content = content.replace("isMovie = true", "isMovie = false")
content = content.replace("category == \"Movies\"", "category == \"Anime\"")
content = content.replace("val categories = listOf(", "val categories = listOf(\n        CategoryItem(\"Anime\", Icons.Default.LocalMovies),")
content = content.replace("CategoryItem(\"Movies\", Icons.Default.LocalMovies),", "")
content = content.replace("\"Movies\"", "\"Anime\"")
content = content.replace("Popular Movies", "Popular Anime")

with open("app/src/main/java/com/example/ui/screens/anime/AnimeScreen.kt", "w") as f:
    f.write(content)
