import re

with open("app/src/main/java/com/example/data/repository/TmdbMediaRepositoryImpl.kt", "r") as f:
    content = f.read()

# We want everything before the messed up part
match = re.search(r"(.*?)    // Add extension functions to map from TMDB models to Domain models", content, re.DOTALL)
if match:
    prefix = match.group(1)
else:
    print("Failed to match")
    exit(1)

suffix = """    // Add extension functions to map from TMDB models to Domain models
    private fun com.example.data.remote.TmdbMovie.toDomain(): Movie {
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
    }

    override suspend fun getSeasonEpisodes(seriesId: String, seasonNumber: Int): List<Episode> = withContext(Dispatchers.IO) {
        try {
            val response = RetrofitClient.tmdbApi.getSeasonDetails(seriesId.toInt(), seasonNumber, apiKey)
            response.episodes?.map {
                Episode(
                    id = it.id.toString(),
                    episodeNumber = it.episodeNumber,
                    title = it.name ?: "Unknown",
                    overview = it.overview ?: "",
                    thumbnailUrl = it.fullStillUrl ?: "",
                    duration = it.runtime ?: 45,
                    rating = it.voteAverage ?: 0.0
                )
            } ?: emptyList()
        } catch (e: Exception) {
            emptyList()
        }
    }

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
}
"""

with open("app/src/main/java/com/example/data/repository/TmdbMediaRepositoryImpl.kt", "w") as f:
    f.write(prefix + suffix)
