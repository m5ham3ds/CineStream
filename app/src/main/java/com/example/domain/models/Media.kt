package com.example.domain.models

data class Movie(
    val id: String,
    val title: String,
    val originalTitle: String? = null,
    val overview: String,
    val posterUrl: String,
    val backdropUrl: String,
    val releaseDate: String? = null,
    val year: Int,
    val rating: Double,
    val genres: List<String>,
    val runtime: Int, // in minutes
    val language: String = "en",
    val country: String? = null,
    val director: String? = null,
    val cast: List<String> = emptyList(),
    val trailerUrl: String? = null
)

data class Series(
    val id: String,
    val title: String,
    val overview: String,
    val posterUrl: String,
    val backdropUrl: String,
    val firstAirDate: String? = null,
    val year: Int,
    val rating: Double,
    val genres: List<String>,
    val seasons: List<Season> = emptyList()
)

data class Season(
    val id: String,
    val seriesId: String,
    val seasonNumber: Int,
    val title: String,
    val posterUrl: String,
    val episodes: List<Episode> = emptyList()
)

data class Episode(
    val id: String,
    val seriesId: String,
    val seasonId: String,
    val episodeNumber: Int,
    val title: String,
    val overview: String,
    val thumbnailUrl: String,
    val duration: Int, // in seconds
    val videoSource: String? = null
)
