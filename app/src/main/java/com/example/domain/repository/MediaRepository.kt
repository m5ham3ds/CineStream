package com.example.domain.repository

import com.example.domain.models.Movie
import com.example.domain.models.Series
import kotlinx.coroutines.flow.Flow

interface MediaRepository {
    fun getMovies(): Flow<List<Movie>>
    fun getSeries(): Flow<List<Series>>
    fun getTrendingMovies(): Flow<List<Movie>>
    fun getTrendingSeries(): Flow<List<Series>>
    suspend fun getMovieById(id: String): Movie?
    suspend fun getSeriesById(id: String): Series?
}
