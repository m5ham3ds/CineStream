import re

with open("app/src/main/java/com/example/data/remote/TmdbApiService.kt", "r") as f:
    content = f.read()

new_api = """
    @GET("movie/upcoming")
    suspend fun getUpcomingMovies(
        @Query("api_key") apiKey: String
    ): TmdbResponse<TmdbMovie>

    @GET("discover/tv")
    suspend fun getAnimeSeries(
        @Query("api_key") apiKey: String,
        @Query("with_genres") withGenres: String = "16",
        @Query("with_original_language") withOriginalLanguage: String = "ja",
        @Query("sort_by") sortBy: String = "popularity.desc"
    ): TmdbResponse<TmdbSeries>
    
    @GET("discover/movie")
    suspend fun getAnimeMovies(
        @Query("api_key") apiKey: String,
        @Query("with_genres") withGenres: String = "16",
        @Query("with_original_language") withOriginalLanguage: String = "ja",
        @Query("sort_by") sortBy: String = "popularity.desc"
    ): TmdbResponse<TmdbMovie>
"""

content = content.replace("    // Search", new_api + "\n    // Search")

with open("app/src/main/java/com/example/data/remote/TmdbApiService.kt", "w") as f:
    f.write(content)
