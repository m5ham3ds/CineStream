import re

filepath = 'app/src/main/java/com/example/domain/providers/ProviderManager.kt'
with open(filepath, 'r') as f:
    content = f.read()

search_code = """
    suspend fun searchProviders(query: String): List<com.example.domain.models.Series> = withContext(Dispatchers.IO) {
        val results = mutableListOf<com.example.domain.models.Series>()
        for (source in sources) {
            try {
                val animeList = source.searchAnime(query, 1)
                animeList.forEach { anime ->
                    val safeTitle = anime.title.replace("|", "")
                    val safeThumb = anime.thumbnailUrl?.replace("|", "") ?: ""
                    results.add(
                        com.example.domain.models.Series(
                            id = "provider|${source.name}|$safeTitle|$safeThumb|${anime.id.replace("|", "")}",
                            title = anime.title,
                            overview = anime.description ?: "",
                            posterUrl = anime.thumbnailUrl,
                            backdropUrl = anime.thumbnailUrl,
                            year = 2024,
                            firstAirDate = "2024",
                            rating = 0.0,
                            genres = emptyList(),
                            seasons = emptyList()
                        )
                    )
                }
            } catch (e: Exception) {
                e.printStackTrace()
            }
        }
        return@withContext results
    }
"""

content = re.sub(r'    suspend fun searchProviders.*?return@withContext results\n    \}', search_code.strip(), content, flags=re.DOTALL)

with open(filepath, 'w') as f:
    f.write(content)
