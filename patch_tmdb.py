import re

with open("app/src/main/java/com/example/data/repository/TmdbMediaRepositoryImpl.kt", "r") as f:
    content = f.read()

new_methods = """
    override fun getUpcomingMovies(): Flow<List<Movie>> = flow {
        try {
            val response = RetrofitClient.tmdbApi.getUpcomingMovies(apiKey)
            emit(response.results.map { it.toDomain() })
        } catch (e: Exception) {
            emit(emptyList())
        }
    }

    override fun getAnimeSeries(): Flow<List<Series>> = flow {
        try {
            val response = RetrofitClient.tmdbApi.getAnimeSeries(apiKey)
            emit(response.results.map { it.toDomain() })
        } catch (e: Exception) {
            emit(emptyList())
        }
    }

    override fun getAnimeMovies(): Flow<List<Movie>> = flow {
        try {
            val response = RetrofitClient.tmdbApi.getAnimeMovies(apiKey)
            emit(response.results.map { it.toDomain() })
        } catch (e: Exception) {
            emit(emptyList())
        }
    }

    override fun getNewReleasesMovies(): Flow<List<Movie>> = flow {
        try {
            val response = RetrofitClient.tmdbApi.getNewReleasesMovies(apiKey)
            emit(response.results.map { it.toDomain() })
        } catch (e: Exception) {
            emit(emptyList())
        }
    }

    override fun getNewReleasesSeries(): Flow<List<Series>> = flow {
        try {
            val response = RetrofitClient.tmdbApi.getNewReleasesSeries(apiKey)
            emit(response.results.map { it.toDomain() })
        } catch (e: Exception) {
            emit(emptyList())
        }
    }
"""
content = content.replace("    override fun getMovies()", new_methods + "\n    override fun getMovies()")

with open("app/src/main/java/com/example/data/repository/TmdbMediaRepositoryImpl.kt", "w") as f:
    f.write(content)
