import re

with open("app/src/main/java/com/example/data/repository/TmdbMediaRepositoryImpl.kt", "r") as f:
    content = f.read()

search_method = """    override suspend fun searchMulti(query: String): Pair<List<Movie>, List<Series>> = withContext(Dispatchers.IO) {
        try {
            val response = RetrofitClient.tmdbApi.searchMulti(apiKey, query)
            val movies = mutableListOf<Movie>()
            val series = mutableListOf<Series>()
            
            response.results.forEach { item ->
                if (item.mediaType == "movie") {
                    movies.add(Movie(
                        id = item.id.toString(),
                        title = item.title ?: "Unknown",
                        overview = "",
                        posterUrl = item.fullPosterUrl,
                        backdropUrl = item.fullBackdropUrl,
                        rating = item.voteAverage ?: 0.0,
                        releaseYear = item.releaseDate?.take(4) ?: "Unknown",
                        genres = emptyList(),
                        duration = ""
                    ))
                } else if (item.mediaType == "tv") {
                    series.add(Series(
                        id = item.id.toString(),
                        title = item.name ?: "Unknown",
                        overview = "",
                        posterUrl = item.fullPosterUrl,
                        backdropUrl = item.fullBackdropUrl,
                        rating = item.voteAverage ?: 0.0,
                        releaseYear = item.firstAirDate?.take(4) ?: "Unknown",
                        genres = emptyList(),
                        seasons = 1
                    ))
                }
            }
            Pair(movies, series)
        } catch (e: Exception) {
            Pair(emptyList(), emptyList())
        }
    }
    
    // Add extension functions to map from TMDB models to Domain models"""

content = content.replace("    // Add extension functions to map from TMDB models to Domain models", search_method)

with open("app/src/main/java/com/example/data/repository/TmdbMediaRepositoryImpl.kt", "w") as f:
    f.write(content)
