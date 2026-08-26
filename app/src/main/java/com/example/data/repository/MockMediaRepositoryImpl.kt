package com.example.data.repository

import com.example.data.mock.MockData
import com.example.domain.models.Movie
import com.example.domain.models.Series
import com.example.domain.repository.MediaRepository
import kotlinx.coroutines.delay
import kotlinx.coroutines.flow.Flow
import kotlinx.coroutines.flow.flow

class MockMediaRepositoryImpl : MediaRepository {
    override fun getMovies(): Flow<List<Movie>> = flow {
        delay(500) // Simulate network delay
        emit(MockData.movies)
    }

    override fun getSeries(): Flow<List<Series>> = flow {
        delay(500)
        emit(MockData.series)
    }

    override fun getTrendingMovies(): Flow<List<Movie>> = flow {
        delay(300)
        emit(MockData.trendingMovies)
    }

    override fun getTrendingSeries(): Flow<List<Series>> = flow {
        delay(300)
        emit(MockData.trendingSeries)
    }

    override suspend fun getMovieById(id: String): Movie? {
        delay(300)
        return MockData.movies.find { it.id == id }
    }

    override suspend fun getSeriesById(id: String): Series? {
        delay(300)
        return MockData.series.find { it.id == id }
    }
}
