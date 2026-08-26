package com.example.navigation

import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.height
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.Menu
import androidx.compose.material.icons.filled.Refresh
import androidx.compose.material3.*
import androidx.compose.runtime.Composable
import androidx.compose.runtime.getValue
import androidx.compose.runtime.rememberCoroutineScope
import androidx.compose.ui.Modifier
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import android.widget.Toast
import kotlinx.coroutines.launch
import androidx.navigation.compose.NavHost
import androidx.navigation.compose.composable
import androidx.navigation.compose.currentBackStackEntryAsState
import androidx.navigation.compose.rememberNavController
import java.net.URLDecoder
import java.net.URLEncoder
import com.example.ui.components.BottomNavBar
import com.example.ui.screens.details.MovieDetailsScreen
import com.example.ui.screens.details.SeriesDetailsScreen
import com.example.ui.screens.home.HomeScreen
import com.example.ui.screens.library.LibraryScreen
import com.example.ui.screens.movies.MoviesScreen
import com.example.ui.screens.search.SearchScreen
import com.example.ui.screens.series.SeriesScreen
import com.example.ui.screens.player.PlayerScreen
import com.example.ui.screens.splash.SplashScreen
import com.example.ui.screens.onboarding.OnboardingScreen
import com.example.ui.screens.profile.ProfileScreen
import com.example.ui.screens.downloads.DownloadsScreen
import com.example.ui.screens.settings.SettingsScreen
import com.example.ui.screens.about.AboutScreen

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun AppNavigation() {
    val navController = rememberNavController()
    val navBackStackEntry by navController.currentBackStackEntryAsState()
    val currentRoute = navBackStackEntry?.destination?.route

    val drawerState = rememberDrawerState(initialValue = DrawerValue.Closed)
    val scope = rememberCoroutineScope()
    val context = LocalContext.current

    val bottomBarRoutes = listOf(
        Screen.Home.route,
        Screen.Movies.route,
        Screen.Series.route,
        Screen.Search.route,
        Screen.Library.route
    )

    ModalNavigationDrawer(
        drawerState = drawerState,
        drawerContent = {
            ModalDrawerSheet {
                Spacer(Modifier.height(12.dp))
                Text(
                    text = "CineStream",
                    style = MaterialTheme.typography.titleLarge,
                    fontWeight = FontWeight.Bold,
                    color = MaterialTheme.colorScheme.primary,
                    modifier = Modifier.padding(16.dp)
                )
                HorizontalDivider()
                
                NavigationDrawerItem(
                    icon = { Icon(Screen.Profile.icon, contentDescription = null) },
                    label = { Text(Screen.Profile.title) },
                    selected = currentRoute == Screen.Profile.route,
                    onClick = {
                        scope.launch { drawerState.close() }
                        navController.navigate(Screen.Profile.route)
                    },
                    modifier = Modifier.padding(horizontal = 12.dp, vertical = 4.dp)
                )
                NavigationDrawerItem(
                    icon = { Icon(Screen.Downloads.icon, contentDescription = null) },
                    label = { Text(Screen.Downloads.title) },
                    selected = currentRoute == Screen.Downloads.route,
                    onClick = {
                        scope.launch { drawerState.close() }
                        navController.navigate(Screen.Downloads.route)
                    },
                    modifier = Modifier.padding(horizontal = 12.dp, vertical = 4.dp)
                )
                NavigationDrawerItem(
                    icon = { Icon(Screen.Settings.icon, contentDescription = null) },
                    label = { Text(Screen.Settings.title) },
                    selected = currentRoute == Screen.Settings.route,
                    onClick = {
                        scope.launch { drawerState.close() }
                        navController.navigate(Screen.Settings.route)
                    },
                    modifier = Modifier.padding(horizontal = 12.dp, vertical = 4.dp)
                )
                NavigationDrawerItem(
                    icon = { Icon(Screen.About.icon, contentDescription = null) },
                    label = { Text(Screen.About.title) },
                    selected = currentRoute == Screen.About.route,
                    onClick = {
                        scope.launch { drawerState.close() }
                        navController.navigate(Screen.About.route)
                    },
                    modifier = Modifier.padding(horizontal = 12.dp, vertical = 4.dp)
                )
                NavigationDrawerItem(
                    icon = { Icon(Icons.Default.Refresh, contentDescription = null) },
                    label = { Text("Check for Updates") },
                    selected = false,
                    onClick = {
                        scope.launch { drawerState.close() }
                        Toast.makeText(context, "You are on the latest version.", Toast.LENGTH_SHORT).show()
                    },
                    modifier = Modifier.padding(horizontal = 12.dp, vertical = 4.dp)
                )
            }
        }
    ) {
        Scaffold(
            topBar = {
                if (bottomBarRoutes.contains(currentRoute) || currentRoute in listOf(Screen.Profile.route, Screen.Downloads.route, Screen.Settings.route, Screen.About.route)) {
                    CenterAlignedTopAppBar(
                        title = { 
                            Text(
                                "CineStream",
                                fontWeight = FontWeight.Bold,
                                color = MaterialTheme.colorScheme.primary
                            ) 
                        },
                        navigationIcon = {
                            IconButton(onClick = { scope.launch { drawerState.open() } }) {
                                Icon(Icons.Default.Menu, contentDescription = "Menu")
                            }
                        },
                        colors = TopAppBarDefaults.centerAlignedTopAppBarColors(
                            containerColor = MaterialTheme.colorScheme.surface
                        )
                    )
                }
            },
            bottomBar = {
                if (bottomBarRoutes.contains(currentRoute)) {
                    BottomNavBar(navController = navController)
                }
            }
        ) { innerPadding ->
            NavHost(
                navController = navController,
                startDestination = Screen.Splash.route,
                modifier = Modifier.padding(innerPadding)
            ) {
                composable(Screen.Splash.route) {
                    SplashScreen(
                        onNavigateToOnboarding = {
                            navController.navigate(Screen.Onboarding.route) {
                                popUpTo(Screen.Splash.route) { inclusive = true }
                            }
                        },
                        onNavigateToHome = {
                            navController.navigate(Screen.Home.route) {
                                popUpTo(Screen.Splash.route) { inclusive = true }
                            }
                        }
                    )
                }
                composable(Screen.Onboarding.route) {
                    OnboardingScreen(
                        onComplete = {
                            navController.navigate(Screen.Home.route) {
                                popUpTo(Screen.Onboarding.route) { inclusive = true }
                            }
                        }
                    )
                }
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
                composable(Screen.Profile.route) { ProfileScreen() }
                composable(Screen.Downloads.route) { DownloadsScreen() }
                composable(Screen.Settings.route) { SettingsScreen() }
                composable(Screen.About.route) { AboutScreen() }
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
}
