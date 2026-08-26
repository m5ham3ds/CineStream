package com.example.navigation

import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.Home
import androidx.compose.material.icons.filled.LibraryBooks
import androidx.compose.material.icons.filled.Movie
import androidx.compose.material.icons.filled.Search
import androidx.compose.material.icons.filled.Tv
import androidx.compose.ui.graphics.vector.ImageVector

sealed class Screen(val route: String, val title: String, val icon: ImageVector) {
    object Home : Screen("home", "Home", Icons.Default.Home)
    object Movies : Screen("movies", "Movies", Icons.Default.Movie)
    object Series : Screen("series", "Series", Icons.Default.Tv)
    object Search : Screen("search", "Search", Icons.Default.Search)
    object Library : Screen("library", "Library", Icons.Default.LibraryBooks)

    object MovieDetails : Screen("movie_details/{movieId}", "Movie Details", Icons.Default.Movie) {
        fun createRoute(movieId: String) = "movie_details/$movieId"
    }
    
    object SeriesDetails : Screen("series_details/{seriesId}", "Series Details", Icons.Default.Tv) {
        fun createRoute(seriesId: String) = "series_details/$seriesId"
    }
}
