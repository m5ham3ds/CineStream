import re

with open("app/src/main/java/com/example/data/repository/TmdbMediaRepositoryImpl.kt", "r") as f:
    content = f.read()

# Update mapping in TmdbMediaRepositoryImpl.kt
new_movie_mapping = """    private fun com.example.data.remote.TmdbMovie.toDomain(): Movie {
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
    }"""

old_mapping_pattern = r"    private fun com\.example\.data\.remote\.TmdbMovie\.toDomain\(\): Movie \{.*?    \}"
content = re.sub(old_mapping_pattern, "", content, flags=re.DOTALL)
old_mapping_pattern2 = r"    private fun com\.example\.data\.remote\.TmdbSeries\.toDomain\(\): Series \{.*?    \}"
content = re.sub(old_mapping_pattern2, new_movie_mapping, content, flags=re.DOTALL)

# Update the searchMulti in TmdbMediaRepositoryImpl
new_search = """                if (item.mediaType == "movie") {
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
                }"""
content = re.sub(r"                if \(item.mediaType == \"movie\"\).*?                \}", new_search, content, flags=re.DOTALL)

with open("app/src/main/java/com/example/data/repository/TmdbMediaRepositoryImpl.kt", "w") as f:
    f.write(content)
