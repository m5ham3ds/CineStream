with open("app/src/main/java/com/example/data/repository/MockMediaRepositoryImpl.kt", "r") as f:
    content = f.read()

new_mock = """
    override fun getUpcomingMovies(): Flow<List<Movie>> = flow { emit(emptyList()) }
    override fun getAnimeSeries(): Flow<List<Series>> = flow { emit(emptyList()) }
    override fun getAnimeMovies(): Flow<List<Movie>> = flow { emit(emptyList()) }
    override fun getNewReleasesMovies(): Flow<List<Movie>> = flow { emit(emptyList()) }
    override fun getNewReleasesSeries(): Flow<List<Series>> = flow { emit(emptyList()) }
"""
content = content.replace("    override suspend fun searchMulti(", new_mock + "\n    override suspend fun searchMulti(")
with open("app/src/main/java/com/example/data/repository/MockMediaRepositoryImpl.kt", "w") as f:
    f.write(content)

