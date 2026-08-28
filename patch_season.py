import re

with open("app/src/main/java/com/example/domain/repository/MediaRepository.kt", "r") as f:
    content = f.read()

if "getSeasonEpisodes" not in content:
    content = content.replace("}", """    suspend fun getSeasonEpisodes(seriesId: String, seasonNumber: Int): List<com.example.domain.models.Episode>\n}""")
    with open("app/src/main/java/com/example/domain/repository/MediaRepository.kt", "w") as f:
        f.write(content)

with open("app/src/main/java/com/example/data/repository/TmdbMediaRepositoryImpl.kt", "r") as f:
    content = f.read()

if "getSeasonEpisodes" not in content:
    impl = """
    override suspend fun getSeasonEpisodes(seriesId: String, seasonNumber: Int): List<Episode> = withContext(Dispatchers.IO) {
        try {
            val response = RetrofitClient.tmdbApi.getSeasonDetails(seriesId.toInt(), seasonNumber, apiKey)
            response.episodes?.map {
                Episode(
                    id = it.id.toString(),
                    episodeNumber = it.episodeNumber,
                    title = it.name ?: "Unknown",
                    overview = it.overview ?: "",
                    thumbnailUrl = it.fullStillUrl ?: "",
                    duration = it.runtime ?: 45,
                    rating = it.voteAverage ?: 0.0
                )
            } ?: emptyList()
        } catch (e: Exception) {
            emptyList()
        }
    }
"""
    content = content.replace("private fun com.example.data.remote.TmdbMovieDetails", impl + "\n    private fun com.example.data.remote.TmdbMovieDetails")
    with open("app/src/main/java/com/example/data/repository/TmdbMediaRepositoryImpl.kt", "w") as f:
        f.write(content)

with open("app/src/main/java/com/example/data/repository/MockMediaRepositoryImpl.kt", "r") as f:
    content = f.read()
if "getSeasonEpisodes" not in content:
    content = content.replace("}", """    override suspend fun getSeasonEpisodes(seriesId: String, seasonNumber: Int): List<com.example.domain.models.Episode> = emptyList()\n}""")
    with open("app/src/main/java/com/example/data/repository/MockMediaRepositoryImpl.kt", "w") as f:
        f.write(content)
