import re

with open("app/src/main/java/com/example/data/repository/TmdbMediaRepositoryImpl.kt", "r") as f:
    content = f.read()

# Add missing imports for new models
imports = """import com.example.domain.models.CastMember
import com.example.domain.models.VideoTrailer
import com.example.domain.models.Season
import com.example.domain.models.Episode
"""
content = content.replace("import kotlinx.coroutines.withContext\n", "import kotlinx.coroutines.withContext\n" + imports)

# We need to change the mappings for getMovieById and getSeriesById to use the Details mappers
# The API methods were changed to return TmdbMovieDetails and TmdbSeriesDetails respectively

# In getMovieById: response is TmdbMovieDetails, so response.toDomainDetails()
content = content.replace("response.toDomain()", "response.toDomainDetails()", 1)

# In getSeriesById: response is TmdbSeriesDetails, so response.toDomainDetails()
content = content.replace("response.toDomain()", "response.toDomainDetails()", 1)


mappers = """
    private fun com.example.data.remote.TmdbMovieDetails.toDomainDetails(): Movie {
        val yearInt = releaseDate?.take(4)?.toIntOrNull() ?: 2024
        return Movie(
            id = id.toString(),
            title = title ?: "Unknown",
            originalTitle = originalTitle,
            overview = overview ?: "",
            posterUrl = fullPosterUrl,
            backdropUrl = fullBackdropUrl,
            year = yearInt,
            releaseDate = releaseDate,
            rating = voteAverage ?: 0.0,
            genres = genres?.map { it.name } ?: emptyList(),
            runtime = runtime ?: 120,
            language = originalLanguage ?: "en",
            cast = credits?.cast?.take(15)?.map { CastMember(it.name, it.character ?: "", it.fullProfileUrl) } ?: emptyList(),
            trailers = videos?.results?.filter { it.site == "YouTube" }?.map { VideoTrailer(it.name, it.key, it.type) } ?: emptyList()
        )
    }

    private fun com.example.data.remote.TmdbSeriesDetails.toDomainDetails(): Series {
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
            genres = genres?.map { it.name } ?: emptyList(),
            cast = credits?.cast?.take(15)?.map { CastMember(it.name, it.character ?: "", it.fullProfileUrl) } ?: emptyList(),
            trailers = videos?.results?.filter { it.site == "YouTube" }?.map { VideoTrailer(it.name, it.key, it.type) } ?: emptyList(),
            seasons = seasons?.map { 
                Season(
                    id = it.id.toString(),
                    seriesId = this.id.toString(),
                    seasonNumber = it.seasonNumber,
                    title = it.name,
                    posterUrl = it.fullPosterUrl ?: fullPosterUrl,
                    episodeCount = it.episodeCount
                ) 
            } ?: emptyList(),
            creator = createdBy?.firstOrNull()?.name,
            status = status
        )
    }
"""

content = content + mappers

with open("app/src/main/java/com/example/data/repository/TmdbMediaRepositoryImpl.kt", "w") as f:
    f.write(content)
