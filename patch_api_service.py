import re

with open("app/src/main/java/com/example/data/remote/TmdbApiService.kt", "r") as f:
    content = f.read()

content = content.replace("): TmdbMovie", "): TmdbMovieDetails")
content = content.replace("): TmdbSeries", "): TmdbSeriesDetails")
# Need to make sure we replace the detail endpoints correctly without breaking list endpoints.

# Wait, let's just rewrite the getMovieDetails and getSeriesDetails functions
old_movie = """    @GET("movie/{movie_id}")
    suspend fun getMovieDetails(
        @Path("movie_id") movieId: Int,
        @Query("api_key") apiKey: String
    ): TmdbMovie"""

new_movie = """    @GET("movie/{movie_id}")
    suspend fun getMovieDetails(
        @Path("movie_id") movieId: Int,
        @Query("api_key") apiKey: String,
        @Query("append_to_response") appendToResponse: String = "credits,videos"
    ): TmdbMovieDetails"""
content = content.replace(old_movie, new_movie)

old_series = """    @GET("tv/{tv_id}")
    suspend fun getSeriesDetails(
        @Path("tv_id") seriesId: Int,
        @Query("api_key") apiKey: String
    ): TmdbSeries"""

new_series = """    @GET("tv/{tv_id}")
    suspend fun getSeriesDetails(
        @Path("tv_id") seriesId: Int,
        @Query("api_key") apiKey: String,
        @Query("append_to_response") appendToResponse: String = "credits,videos"
    ): TmdbSeriesDetails
    
    @GET("tv/{tv_id}/season/{season_number}")
    suspend fun getSeasonDetails(
        @Path("tv_id") seriesId: Int,
        @Path("season_number") seasonNumber: Int,
        @Query("api_key") apiKey: String
    ): TmdbSeasonDetails"""
content = content.replace(old_series, new_series)

with open("app/src/main/java/com/example/data/remote/TmdbApiService.kt", "w") as f:
    f.write(content)
