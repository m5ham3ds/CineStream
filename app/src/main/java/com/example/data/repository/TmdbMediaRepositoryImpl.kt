package com.example.data.repository

import com.example.BuildConfig
import com.example.data.remote.RetrofitClient
import com.example.domain.models.Movie
import com.example.domain.models.Series
import com.example.domain.repository.MediaRepository
import kotlinx.coroutines.flow.Flow
import kotlinx.coroutines.flow.flow
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.withContext

class TmdbMediaRepositoryImpl : MediaRepository {
    
    // Fallback to empty string if missing
    private val apiKey = BuildConfig.TMDB_API_KEY

    override fun getMovies(): Flow<List<Movie>> = flow {
        try {
            val response = RetrofitClient.tmdbApi.getPopularMovies(apiKey)
            emit(response.results.map { it.toDomain() })
        } catch (e: Exception) {
            emit(emptyList())
        }
    }

    override fun getSeries(): Flow<List<Series>> = flow {
        try {
            val response = RetrofitClient.tmdbApi.getPopularSeries(apiKey)
            emit(response.results.map { it.toDomain() })
        } catch (e: Exception) {
            emit(emptyList())
        }
    }

    override fun getTrendingMovies(): Flow<List<Movie>> = flow {
        try {
            val response = RetrofitClient.tmdbApi.getTrendingMovies(apiKey)
            emit(response.results.map { it.toDomain() })
        } catch (e: Exception) {
            emit(emptyList())
        }
    }

    override fun getTrendingSeries(): Flow<List<Series>> = flow {
        try {
            val response = RetrofitClient.tmdbApi.getTrendingSeries(apiKey)
            emit(response.results.map { it.toDomain() })
        } catch (e: Exception) {
            emit(emptyList())
        }
    }

    override suspend fun getMovieById(id: String): Movie? = withContext(Dispatchers.IO) {
        try {
            val response = RetrofitClient.tmdbApi.getMovieDetails(id.toInt(), apiKey)
            response.toDomain()
        } catch (e: Exception) {
            null
        }
    }

    override suspend fun getSeriesById(id: String): Series? = withContext(Dispatchers.IO) {
        try {
            val response = RetrofitClient.tmdbApi.getSeriesDetails(id.toInt(), apiKey)
            response.toDomain()
        } catch (e: Exception) {
            null
        }
    }
    
    override suspend fun searchMulti(query: String): Pair<List<Movie>, List<Series>> = withContext(Dispatchers.IO) {
        try {
            val response = RetrofitClient.tmdbApi.searchMulti(apiKey, query)
            val movies = mutableListOf<Movie>()
            val series = mutableListOf<Series>()
            
            response.results.forEach { item ->
                if (item.mediaType == "movie") {
                    val yearInt = item.releaseDate?.take(4)?.toIntOrNull() ?: 2024
                    movies.add(Movie(
                        id = item.id.toString(),
                        title = item.title ?: "Unknown",
                        overview = "",
                        posterUrl = item.fullPosterUrl,
                        backdropUrl = item.fullBackdropUrl,
                        year = yearInt,
                        releaseDate = item.releaseDate,
                        rating = item.voteAverage ?: 0.0,
                        genres = emptyList(),
                        runtime = 120
                    ))
                } else if (item.mediaType == "tv") {
                    val yearInt = item.firstAirDate?.take(4)?.toIntOrNull() ?: 2024
                    series.add(Series(
                        id = item.id.toString(),
                        title = item.name ?: "Unknown",
                        overview = "",
                        posterUrl = item.fullPosterUrl,
                        backdropUrl = item.fullBackdropUrl,
                        year = yearInt,
                        firstAirDate = item.firstAirDate,
                        rating = item.voteAverage ?: 0.0,
                        genres = emptyList(),
                        seasons = emptyList()
                    ))
                }
            }
            Pair(movies, series)
        } catch (e: Exception) {
            Pair(emptyList(), emptyList())
        }
    }
    
    // Add extension functions to map from TMDB models to Domain models

    
    private fun com.example.data.remote.TmdbMovie.toDomain(): Movie {
        val yearInt = releaseDate?.take(4)?.toIntOrNull() ?: 2024
        return Movie(
            id = id.toString(),
            title = title ?: "Unknown",
            overview = overview ?: "",
            posterUrl = fullPosterUrl,
            backdropUrl = fullBackdropUrl,
            year = yearInt,
            releaseDate = releaseDate,
            rating = voteAverage ?: 0.0,
            genres = emptyList(),
            runtime = 120
        )
    }
    
    private fun com.example.data.remote.TmdbSeries.toDomain(): Series {
        val yearInt = firstAirDate?.take(4)?.toIntOrNull() ?: 2024
        return Series(
            id = id.toString(),
            title = name ?: "Unknown",
            overview = overview ?: "",
            posterUrl = fullPosterUrl,
            backdropUrl = fullBackdropUrl,
            year = yearInt,
            firstAirDate = firstAirDate,
            rating = voteAverage ?: 0.0,
            genres = emptyList(),
            seasons = emptyList()
        )
    }
}
