import re

# 1. Fix TmdbApiService.kt
with open("app/src/main/java/com/example/data/remote/TmdbApiService.kt", "r") as f:
    content = f.read()
content = content.replace("TmdbMovieDetailsDetails", "TmdbMovieDetails")
content = content.replace("TmdbSeasonDetailsDetails", "TmdbSeasonDetails")
content = content.replace("TmdbSeriesDetailsDetails", "TmdbSeriesDetails")
with open("app/src/main/java/com/example/data/remote/TmdbApiService.kt", "w") as f:
    f.write(content)

# 2. Fix MockMediaRepositoryImpl.kt
# It got messed up by my replace. I'll just rewrite it entirely.
mock_repo_content = """package com.example.data.repository

import com.example.domain.models.Movie
import com.example.domain.models.Series
import com.example.domain.models.Episode
import com.example.domain.repository.MediaRepository
import kotlinx.coroutines.flow.Flow
import kotlinx.coroutines.flow.flow

class MockMediaRepositoryImpl : MediaRepository {
    override fun getMovies(): Flow<List<Movie>> = flow {
        emit(emptyList())
    }
    override fun getSeries(): Flow<List<Series>> = flow {
        emit(emptyList())
    }
    override fun getTrendingMovies(): Flow<List<Movie>> = flow {
        emit(emptyList())
    }
    override fun getTrendingSeries(): Flow<List<Series>> = flow {
        emit(emptyList())
    }
    override suspend fun getMovieById(id: String): Movie? = null
    override suspend fun getSeriesById(id: String): Series? = null
    override suspend fun searchMulti(query: String): Pair<List<Movie>, List<Series>> = Pair(emptyList(), emptyList())
    override suspend fun getSeasonEpisodes(seriesId: String, seasonNumber: Int): List<Episode> = emptyList()
}
"""
with open("app/src/main/java/com/example/data/repository/MockMediaRepositoryImpl.kt", "w") as f:
    f.write(mock_repo_content)

# 3. Fix MockData.kt (just empty it out or fix imports, we are using TMDB anyway)
mock_data_content = """package com.example.data.mock
// Removed to fix build errors since we don't use it anymore
"""
with open("app/src/main/java/com/example/data/mock/MockData.kt", "w") as f:
    f.write(mock_data_content)

# 4. Fix TmdbMediaRepositoryImpl.kt (getSeasonEpisodes is outside class)
with open("app/src/main/java/com/example/data/repository/TmdbMediaRepositoryImpl.kt", "r") as f:
    content = f.read()

# Remove the bad getSeasonEpisodes
bad_episodes = re.search(r"override suspend fun getSeasonEpisodes.*?\}", content, re.DOTALL)
if bad_episodes:
    content = content.replace(bad_episodes.group(0), "")

# Let's insert getSeasonEpisodes right before the `toDomainDetails` functions inside the class
if "override suspend fun getSeasonEpisodes" not in content:
    get_season_episodes = """
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
    content = content.replace("private fun com.example.data.remote.TmdbMovieDetails.toDomainDetails", get_season_episodes + "\n    private fun com.example.data.remote.TmdbMovieDetails.toDomainDetails")
with open("app/src/main/java/com/example/data/repository/TmdbMediaRepositoryImpl.kt", "w") as f:
    f.write(content)
