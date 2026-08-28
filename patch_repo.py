import re

with open("app/src/main/java/com/example/data/repository/TmdbMediaRepositoryImpl.kt", "r") as f:
    content = f.read()

# Make sure imports are present
imports_str = """import com.example.domain.models.PersonDetails"""
if "PersonDetails" not in content:
    content = content.replace("import com.example.domain.models.Episode", "import com.example.domain.models.Episode\n" + imports_str)

# Filter trailers -> only "Trailer" type and "YouTube" site.
# In `toDomainDetails` for Movie:
content = content.replace(
    """trailers = videos?.results?.filter { it.site == "YouTube" }?.map { VideoTrailer(it.name, it.key, it.type) } ?: emptyList()""",
    """trailers = videos?.results?.filter { it.site == "YouTube" && it.type == "Trailer" }?.map { VideoTrailer(it.name, it.key, it.type) } ?: emptyList()"""
)
# Note: we need CastMember to include `it.id.toString()` since we added `id` to CastMember.
content = content.replace(
    """cast = credits?.cast?.take(15)?.map { CastMember(it.name, it.character ?: "", it.fullProfileUrl) } ?: emptyList()""",
    """cast = credits?.cast?.take(15)?.map { CastMember(it.id.toString(), it.name, it.character ?: "", it.fullProfileUrl) } ?: emptyList()"""
)

# And now add the `getPersonDetails`
get_person_details = """
    override suspend fun getPersonDetails(personId: String): PersonDetails? = withContext(Dispatchers.IO) {
        try {
            val response = RetrofitClient.tmdbApi.getPersonDetails(personId.toInt(), apiKey)
            val movies = mutableListOf<Movie>()
            val series = mutableListOf<Series>()
            response.combinedCredits?.cast?.forEach { item ->
                if (item.mediaType == "movie") {
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
                }
            }
            
            PersonDetails(
                id = response.id.toString(),
                name = response.name ?: "Unknown",
                biography = response.biography ?: "",
                profileUrl = response.fullProfileUrl,
                birthday = response.birthday,
                placeOfBirth = response.placeOfBirth,
                knownFor = response.knownForDepartment,
                movies = movies,
                series = series
            )
        } catch (e: Exception) {
            null
        }
    }
"""

if "override suspend fun getPersonDetails" not in content:
    content = content.replace("override suspend fun getSeasonEpisodes", get_person_details + "\n    override suspend fun getSeasonEpisodes")

with open("app/src/main/java/com/example/data/repository/TmdbMediaRepositoryImpl.kt", "w") as f:
    f.write(content)
