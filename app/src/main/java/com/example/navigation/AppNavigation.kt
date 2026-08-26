package com.example.navigation

import androidx.compose.foundation.layout.padding
import androidx.compose.material3.Scaffold
import androidx.compose.runtime.Composable
import androidx.compose.runtime.getValue
import androidx.compose.ui.Modifier
import androidx.navigation.compose.NavHost
import androidx.navigation.compose.composable
import androidx.navigation.compose.currentBackStackEntryAsState
import androidx.navigation.compose.rememberNavController
import com.example.ui.components.BottomNavBar
import com.example.ui.screens.details.MovieDetailsScreen
import com.example.ui.screens.details.SeriesDetailsScreen
import com.example.ui.screens.home.HomeScreen
import com.example.ui.screens.library.LibraryScreen
import com.example.ui.screens.movies.MoviesScreen
import com.example.ui.screens.search.SearchScreen
import com.example.ui.screens.series.SeriesScreen
import com.example.ui.screens.player.PlayerScreen
import java.net.URLDecoder
import java.net.URLEncoder

@Composable
fun AppNavigation() {
    val navController = rememberNavController()
    val navBackStackEntry by navController.currentBackStackEntryAsState()
    val currentRoute = navBackStackEntry?.destination?.route

    val bottomBarRoutes = listOf(
        Screen.Home.route,
        Screen.Movies.route,
        Screen.Series.route,
        Screen.Search.route,
        Screen.Library.route
    )

    Scaffold(
        bottomBar = {
            if (bottomBarRoutes.contains(currentRoute)) {
                BottomNavBar(navController = navController)
            }
        }
    ) { innerPadding ->
        NavHost(
            navController = navController,
            startDestination = Screen.Home.route,
            modifier = Modifier.padding(innerPadding)
        ) {
            composable(Screen.Home.route) {
                HomeScreen(
                    onMovieClick = { id -> navController.navigate(Screen.MovieDetails.createRoute(id)) },
                    onSeriesClick = { id -> navController.navigate(Screen.SeriesDetails.createRoute(id)) }
                )
            }
            composable(Screen.Movies.route) {
                MoviesScreen(
                    onMovieClick = { id -> navController.navigate(Screen.MovieDetails.createRoute(id)) }
                )
            }
            composable(Screen.Series.route) {
                SeriesScreen(
                    onSeriesClick = { id -> navController.navigate(Screen.SeriesDetails.createRoute(id)) }
                )
            }
            composable(Screen.Search.route) {
                SearchScreen(
                    onMediaClick = { id, isMovie ->
                        if (isMovie) {
                            navController.navigate(Screen.MovieDetails.createRoute(id))
                        } else {
                            navController.navigate(Screen.SeriesDetails.createRoute(id))
                        }
                    }
                )
            }
            composable(Screen.Library.route) {
                LibraryScreen()
            }
            composable(Screen.MovieDetails.route) { backStackEntry ->
                val movieId = backStackEntry.arguments?.getString("movieId") ?: return@composable
                MovieDetailsScreen(
                    movieId = movieId, 
                    onBack = { navController.popBackStack() },
                    onPlay = { url -> 
                        val encodedUrl = URLEncoder.encode(url, "UTF-8")
                        navController.navigate("player/$encodedUrl")
                    }
                )
            }
            composable(Screen.SeriesDetails.route) { backStackEntry ->
                val seriesId = backStackEntry.arguments?.getString("seriesId") ?: return@composable
                SeriesDetailsScreen(
                    seriesId = seriesId, 
                    onBack = { navController.popBackStack() },
                    onPlay = { url -> 
                        val encodedUrl = URLEncoder.encode(url, "UTF-8")
                        navController.navigate("player/$encodedUrl")
                    }
                )
            }
            composable("player/{url}") { backStackEntry ->
                val url = backStackEntry.arguments?.getString("url") ?: return@composable
                val decodedUrl = URLDecoder.decode(url, "UTF-8")
                PlayerScreen(videoUrl = decodedUrl, onBack = { navController.popBackStack() })
            }
        }
    }
}
