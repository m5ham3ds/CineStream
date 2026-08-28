import re

# Fix MockMediaRepositoryImpl
with open("app/src/main/java/com/example/data/repository/MockMediaRepositoryImpl.kt", "r") as f:
    content = f.read()

new_mock = """
    override fun getUpcomingMovies(): Flow<List<Movie>> = flowOf(emptyList())
    override fun getAnimeSeries(): Flow<List<Series>> = flowOf(emptyList())
    override fun getAnimeMovies(): Flow<List<Movie>> = flowOf(emptyList())
    override fun getNewReleasesMovies(): Flow<List<Movie>> = flowOf(emptyList())
    override fun getNewReleasesSeries(): Flow<List<Series>> = flowOf(emptyList())
"""
content = content.replace("    override fun search(", new_mock + "\n    override fun search(")
with open("app/src/main/java/com/example/data/repository/MockMediaRepositoryImpl.kt", "w") as f:
    f.write(content)

# Fix AnimeScreen
with open("app/src/main/java/com/example/ui/screens/anime/AnimeScreen.kt", "r") as f:
    content = f.read()

content = content.replace("year = series.year,", "year = series.year.toString(),")
with open("app/src/main/java/com/example/ui/screens/anime/AnimeScreen.kt", "w") as f:
    f.write(content)

# Fix HomeScreen
with open("app/src/main/java/com/example/ui/screens/home/HomeScreen.kt", "r") as f:
    content = f.read()

content = content.replace("year = series.year,", "year = series.year.toString(),")
content = content.replace("year = movie.year,", "year = movie.year.toString(),")
content = content.replace("year = item.year,", "year = item.year.toString(),")

# Fix line 271: Movie(it.id, it.title, it.overview, it.posterUrl, it.backdropUrl, it.rating, it.year, it.genres)
# Wait, Movie constructor:
# Movie(id, title, originalTitle?, overview, posterUrl, backdropUrl, releaseDate?, year, rating, genres, runtime, language, country, director, cast, trailers)
# originalTitle = null, releaseDate = null, runtime = 0, language="en", etc.
movie_mapping = "Movie(id = it.id, title = it.title, overview = it.overview, posterUrl = it.posterUrl, backdropUrl = it.backdropUrl, year = it.year, rating = it.rating, genres = it.genres, runtime = 0)"
content = content.replace("Movie(it.id, it.title, it.overview, it.posterUrl, it.backdropUrl, it.rating, it.year, it.genres)", movie_mapping)

with open("app/src/main/java/com/example/ui/screens/home/HomeScreen.kt", "w") as f:
    f.write(content)

