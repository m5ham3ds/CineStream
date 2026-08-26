package com.example.data.mock

import com.example.domain.models.*

object MockData {
    val movies = (1..10).map {
        Movie(
            id = "movie_$it",
            title = "Demo Movie ${it.toString().padStart(2, '0')}",
            overview = "This is a brief description for Demo Movie $it. It features an exciting plot and amazing visuals, taking you on an unforgettable journey.",
            posterUrl = "https://picsum.photos/seed/movie_poster_$it/300/450",
            backdropUrl = "https://picsum.photos/seed/movie_backdrop_$it/800/450",
            year = 2020 + (it % 5),
            rating = 7.0 + (it % 3),
            genres = listOf("Action", "Sci-Fi", "Drama").take((it % 3) + 1),
            runtime = 120 + (it * 2),
            cast = listOf("Actor A", "Actor B", "Actor C")
        )
    }

    val episodes = (1..5).map { ep ->
        Episode(
            id = "ep_$ep",
            seriesId = "series_tmp",
            seasonId = "season_tmp",
            episodeNumber = ep,
            title = "Episode $ep",
            overview = "This is episode $ep of the amazing series.",
            thumbnailUrl = "https://picsum.photos/seed/ep_${ep}/400/225",
            duration = 2700,
            videoSource = "https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/BigBuckBunny.mp4"
        )
    }

    val seasons = (1..3).map { s ->
        Season(
            id = "season_$s",
            seriesId = "series_tmp",
            seasonNumber = s,
            title = "Season $s",
            posterUrl = "https://picsum.photos/seed/season_$s/300/450",
            episodes = episodes.map { it.copy(id = "ep_${s}_${it.episodeNumber}", seasonId = "season_$s") }
        )
    }

    val series = (1..10).map {
        Series(
            id = "series_$it",
            title = "Demo Series ${it.toString().padStart(2, '0')}",
            overview = "This is an amazing Demo Series $it filled with suspense, drama, and action.",
            posterUrl = "https://picsum.photos/seed/series_poster_$it/300/450",
            backdropUrl = "https://picsum.photos/seed/series_backdrop_$it/800/450",
            year = 2018 + (it % 6),
            rating = 8.0 + (it % 2),
            genres = listOf("Drama", "Thriller").take((it % 2) + 1),
            seasons = seasons.map { s -> s.copy(seriesId = "series_$it") }
        )
    }

    val trendingMovies = movies.shuffled().take(5)
    val trendingSeries = series.shuffled().take(5)
    val actionMovies = movies.filter { it.genres.contains("Action") }
    val recommended = movies.shuffled().take(3)
}
