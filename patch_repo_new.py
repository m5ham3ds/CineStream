import re

with open("app/src/main/java/com/example/domain/repository/MediaRepository.kt", "r") as f:
    content = f.read()

new_methods = """
    fun getNewReleasesMovies(): Flow<List<Movie>>
    fun getNewReleasesSeries(): Flow<List<Series>>
"""

content = content.replace("    fun getAnimeMovies(): Flow<List<Movie>>", "    fun getAnimeMovies(): Flow<List<Movie>>\n" + new_methods)

with open("app/src/main/java/com/example/domain/repository/MediaRepository.kt", "w") as f:
    f.write(content)


with open("app/src/main/java/com/example/data/repository/TmdbMediaRepositoryImpl.kt", "r") as f:
    impl_content = f.read()

new_impl = """
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

impl_content = impl_content.replace("    override fun search(", new_impl + "\n    override fun search(")

with open("app/src/main/java/com/example/data/repository/TmdbMediaRepositoryImpl.kt", "w") as f:
    f.write(impl_content)
