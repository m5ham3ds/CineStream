package com.example.data.remote

import retrofit2.http.GET
import retrofit2.http.Query
import retrofit2.http.Path

interface TmdbApiService {

    // Movies
    @GET("trending/movie/day")
    suspend fun getTrendingMovies(
        @Query("api_key") apiKey: String
    ): TmdbResponse<TmdbMovie>
    
    @GET("movie/popular")
    suspend fun getPopularMovies(
        @Query("api_key") apiKey: String
    ): TmdbResponse<TmdbMovie>
    
    @GET("movie/now_playing")
    suspend fun getNewReleasesMovies(
        @Query("api_key") apiKey: String
    ): TmdbResponse<TmdbMovie>

    @GET("movie/{movie_id}")
    suspend fun getMovieDetails(
        @Path("movie_id") movieId: Int,
        @Query("api_key") apiKey: String
    ): TmdbMovie

    // Series
    @GET("trending/tv/day")
    suspend fun getTrendingSeries(
        @Query("api_key") apiKey: String
    ): TmdbResponse<TmdbSeries>
    
    @GET("tv/popular")
    suspend fun getPopularSeries(
        @Query("api_key") apiKey: String
    ): TmdbResponse<TmdbSeries>
    
    @GET("tv/on_the_air")
    suspend fun getNewReleasesSeries(
        @Query("api_key") apiKey: String
    ): TmdbResponse<TmdbSeries>

    @GET("tv/{tv_id}")
    suspend fun getSeriesDetails(
        @Path("tv_id") seriesId: Int,
        @Query("api_key") apiKey: String
    ): TmdbSeries
    
    // Search
    @GET("search/multi")
    suspend fun searchMulti(
        @Query("api_key") apiKey: String,
        @Query("query") query: String
    ): TmdbResponse<TmdbMulti>
}
