import re

filepath = 'app/src/main/java/com/example/data/repository/TmdbMediaRepositoryImpl.kt'
with open(filepath, 'r') as f:
    content = f.read()

# Fix Movie
movie_by_id = """
    override suspend fun getMovieById(id: String): Movie? = withContext(Dispatchers.IO) {
        if (id.startsWith("provider|")) {
            val parts = id.split("|")
            val title = parts.getOrNull(2) ?: "Unknown"
            val thumb = parts.getOrNull(3) ?: ""
            return@withContext Movie(
                id = id,
                title = title,
                originalTitle = title,
                overview = "Content from provider ${parts.getOrNull(1) ?: "Unknown"}",
                posterUrl = thumb,
                backdropUrl = thumb,
                year = 2024,
                releaseDate = "2024",
                rating = 0.0,
                genres = emptyList(),
                runtime = 0,
                language = "en",
                cast = emptyList(),
                trailers = emptyList()
            )
        }
        try {
            val response = RetrofitClient.tmdbApi.getMovieDetails(id.toInt(), apiKey)
            response.toDomainDetails()
        } catch (e: Exception) {
            null
        }
    }
"""

# Fix Series
series_by_id = """
    override suspend fun getSeriesById(id: String): Series? = withContext(Dispatchers.IO) {
        if (id.startsWith("provider|")) {
            val parts = id.split("|")
            val title = parts.getOrNull(2) ?: "Unknown"
            val thumb = parts.getOrNull(3) ?: ""
            return@withContext Series(
                id = id,
                title = title,
                overview = "Content from provider ${parts.getOrNull(1) ?: "Unknown"}",
                posterUrl = thumb,
                backdropUrl = thumb,
                year = 2024,
                firstAirDate = "2024",
                rating = 0.0,
                genres = emptyList(),
                cast = emptyList(),
                trailers = emptyList(),
                seasons = emptyList(),
                creator = parts.getOrNull(1) ?: "Unknown",
                status = "Unknown"
            )
        }
        try {
            val response = RetrofitClient.tmdbApi.getSeriesDetails(id.toInt(), apiKey)
            response.toDomainDetails()
        } catch (e: Exception) {
            null
        }
    }
"""

content = re.sub(r'    override suspend fun getMovieById.*?\}\n    \}', movie_by_id.strip(), content, flags=re.DOTALL)
content = re.sub(r'    override suspend fun getSeriesById.*?\}\n    \}', series_by_id.strip(), content, flags=re.DOTALL)

with open(filepath, 'w') as f:
    f.write(content)

# Fix ProviderManager
filepath = 'app/src/main/java/com/example/domain/providers/ProviderManager.kt'
with open(filepath, 'r') as f:
    content = f.read()

search_code = """
                        com.example.domain.models.Series(
                            id = "provider|${source.name}|$safeTitle|$safeThumb|${anime.id.replace("|", "")}",
                            title = anime.title,
                            overview = anime.description ?: "",
                            posterUrl = safeThumb,
                            backdropUrl = safeThumb,
                            year = 2024,
                            firstAirDate = "2024",
                            rating = 0.0,
                            genres = emptyList(),
                            seasons = emptyList()
                        )
"""
content = re.sub(r'                        com\.example\.domain\.models\.Series\(\n                            id = "provider.*?seasons = emptyList\(\)\n                        \)', search_code.strip(), content, flags=re.DOTALL)

with open(filepath, 'w') as f:
    f.write(content)

