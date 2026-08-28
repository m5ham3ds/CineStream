with open("app/src/main/java/com/example/data/remote/TmdbModels.kt", "a") as f:
    f.write("""

@JsonClass(generateAdapter = true)
data class TmdbPersonMovieCredit(
    @Json(name = "id") val id: Int,
    @Json(name = "title") val title: String?,
    @Json(name = "overview") val overview: String?,
    @Json(name = "poster_path") val posterPath: String?,
    @Json(name = "backdrop_path") val backdropPath: String?,
    @Json(name = "release_date") val releaseDate: String?,
    @Json(name = "vote_average") val voteAverage: Double?
) {
    val fullPosterUrl: String
        get() = posterPath?.let { "https://image.tmdb.org/t/p/w500$it" } ?: ""
}

@JsonClass(generateAdapter = true)
data class TmdbPersonSeriesCredit(
    @Json(name = "id") val id: Int,
    @Json(name = "name") val name: String?,
    @Json(name = "overview") val overview: String?,
    @Json(name = "poster_path") val posterPath: String?,
    @Json(name = "backdrop_path") val backdropPath: String?,
    @Json(name = "first_air_date") val firstAirDate: String?,
    @Json(name = "vote_average") val voteAverage: Double?
) {
    val fullPosterUrl: String
        get() = posterPath?.let { "https://image.tmdb.org/t/p/w500$it" } ?: ""
}

@JsonClass(generateAdapter = true)
data class TmdbPersonCombinedCredits(
    @Json(name = "cast") val cast: List<TmdbMulti> // We can reuse TmdbMulti since it handles both movie/tv
)

@JsonClass(generateAdapter = true)
data class TmdbPersonDetails(
    @Json(name = "id") val id: Int,
    @Json(name = "name") val name: String?,
    @Json(name = "biography") val biography: String?,
    @Json(name = "profile_path") val profilePath: String?,
    @Json(name = "birthday") val birthday: String?,
    @Json(name = "place_of_birth") val placeOfBirth: String?,
    @Json(name = "known_for_department") val knownForDepartment: String?,
    @Json(name = "combined_credits") val combinedCredits: TmdbPersonCombinedCredits?
) {
    val fullProfileUrl: String?
        get() = profilePath?.let { "https://image.tmdb.org/t/p/w500$it" }
}
""")
