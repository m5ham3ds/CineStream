package com.example.navigation

import androidx.compose.foundation.Image
import androidx.compose.foundation.background
import androidx.compose.foundation.border
import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.shape.CircleShape
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.automirrored.filled.ExitToApp
import androidx.compose.material.icons.automirrored.filled.Help
import androidx.compose.material.icons.filled.Home
import androidx.compose.material.icons.filled.Favorite
import androidx.compose.material.icons.filled.Menu
import androidx.compose.material.icons.filled.Notifications
import androidx.compose.material.icons.filled.Person
import androidx.compose.material.icons.filled.Refresh
import androidx.compose.material.icons.filled.KeyboardArrowDown
import androidx.compose.material.icons.outlined.Notifications
import androidx.compose.material.icons.outlined.Settings
import androidx.compose.material.icons.outlined.Info
import androidx.compose.material.icons.filled.Search
import androidx.compose.material.icons.outlined.Search
import androidx.compose.material.icons.outlined.Download
import androidx.compose.material3.*
import androidx.compose.runtime.Composable
import androidx.compose.runtime.getValue
import androidx.compose.runtime.remember
import androidx.compose.runtime.setValue
import androidx.compose.runtime.rememberCoroutineScope
import androidx.compose.runtime.collectAsState
import androidx.compose.runtime.mutableStateOf
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.graphics.Brush
import androidx.compose.ui.layout.ContentScale
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.res.painterResource
import androidx.compose.ui.text.font.FontFamily
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.style.TextAlign
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
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
import com.example.ui.screens.home.PopularScreen
import com.example.ui.screens.home.NewReleasesScreen
import com.example.ui.screens.home.TrendingScreen
import com.example.ui.screens.home.WatchingScreen
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
import com.example.ui.screens.auth.AuthScreen

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun AppNavigation() {
    val navController = rememberNavController()
    val navBackStackEntry by navController.currentBackStackEntryAsState()
    val currentRoute = navBackStackEntry?.destination?.route

    val drawerState = rememberDrawerState(initialValue = DrawerValue.Closed)
    val scope = rememberCoroutineScope()
    val context = LocalContext.current
    
    val userPrefs = remember { com.example.data.repository.UserPreferencesRepository(context) }
    val isGuest by userPrefs.isGuest.collectAsState(initial = false)
    
    var isSearchExpanded by androidx.compose.runtime.remember { androidx.compose.runtime.mutableStateOf(false) }
    var searchQuery by androidx.compose.runtime.remember { androidx.compose.runtime.mutableStateOf("") }
    var showLogoutDialog by androidx.compose.runtime.remember { androidx.compose.runtime.mutableStateOf(false) }

    val bottomBarRoutes = listOf(
        Screen.Home.route,
        Screen.Movies.route,
        Screen.Series.route,
        Screen.Search.route,
        Screen.Library.route
    )

    androidx.compose.runtime.CompositionLocalProvider(androidx.compose.ui.platform.LocalLayoutDirection provides androidx.compose.ui.unit.LayoutDirection.Rtl) {
    ModalNavigationDrawer(
        drawerState = drawerState,
        gesturesEnabled = drawerState.isOpen,
        drawerContent = {
            ModalDrawerSheet(
                drawerContainerColor = Color(0xFF161618),
                modifier = Modifier.width(300.dp)
            ) {
                // Top Header Section with Gradient
                Box(
                    modifier = Modifier
                        .fillMaxWidth()
                        .height(200.dp)
                        .background(
                            brush = Brush.verticalGradient(
                                colors = listOf(Color(0xFF2B2B2B), Color(0xFF161618))
                            )
                        )
                        .padding(16.dp)
                ) {
                    Column(
                        modifier = Modifier.fillMaxSize(),
                        verticalArrangement = Arrangement.Top
                    ) {
                        Text(
                            text = "CineStream",
                            style = MaterialTheme.typography.headlineMedium.copy(
                                fontWeight = FontWeight.Bold,
                                fontFamily = FontFamily.Serif
                            ),
                            color = Color(0xFFE50914),
                            modifier = Modifier.fillMaxWidth(),
                            textAlign = TextAlign.Start
                        )
                        Spacer(modifier = Modifier.weight(1f))
                        Row(
                            verticalAlignment = Alignment.CenterVertically,
                            modifier = Modifier.clickable {
                                scope.launch { drawerState.close() }
                                if (isGuest) {
                                    navController.navigate(Screen.Auth.route)
                                } else {
                                    navController.navigate(Screen.Profile.route)
                                }
                            }
                        ) {
                            Column {
                                Text(
                                    text = if (isGuest) "Guest User" else "E. Laurent",
                                    fontSize = 24.sp,
                                    fontFamily = FontFamily.SansSerif,
                                    color = Color.White
                                )
                                Row(verticalAlignment = Alignment.CenterVertically) {
                                    if (!isGuest) {
                                        Icon(painter = painterResource(android.R.drawable.ic_dialog_info), contentDescription = null, tint = Color(0xFFE50914), modifier = Modifier.size(16.dp))
                                        Spacer(modifier = Modifier.width(4.dp))
                                    }
                                    Text(
                                        text = if (isGuest) "Free Account" else "Premium User",
                                        fontSize = 14.sp,
                                        color = Color.LightGray
                                    )
                                }
                            }
                            Spacer(modifier = Modifier.weight(1f))
                            Box(
                                modifier = Modifier
                                    .size(70.dp)
                                    .clip(CircleShape)
                                    .background(Color.Gray)
                                    .border(2.dp, Color(0xFFE50914), CircleShape),
                                contentAlignment = Alignment.Center
                            ) {
                                Icon(Icons.Default.Person, contentDescription = "Avatar", tint = Color.White, modifier = Modifier.size(40.dp))
                            }
                        }
                    }
                }
                
                Spacer(modifier = Modifier.height(16.dp))
                
                NavigationDrawerItem(
                    icon = { Icon(Icons.Default.Home, contentDescription = null, tint = if (currentRoute == Screen.Home.route) Color(0xFFE50914) else Color.White) },
                    label = { Text("الرئيسية", color = Color.White, fontSize = 16.sp) },
                    selected = currentRoute == Screen.Home.route,
                    colors = NavigationDrawerItemDefaults.colors(
                        selectedContainerColor = Color(0xFFE50914).copy(alpha = 0.2f),
                        unselectedContainerColor = Color.Transparent
                    ),
                    shape = RoundedCornerShape(16.dp),
                    onClick = {
                        scope.launch { drawerState.close() }
                        navController.navigate(Screen.Home.route)
                    },
                    modifier = Modifier.padding(horizontal = 16.dp, vertical = 8.dp)
                )

                NavigationDrawerItem(
                    icon = { Icon(Icons.Outlined.Download, contentDescription = null, tint = Color.White) },
                    label = { Text("التنزيلات", color = Color.White, fontSize = 16.sp) },
                    selected = currentRoute == Screen.Downloads.route,
                    colors = NavigationDrawerItemDefaults.colors(unselectedContainerColor = Color.Transparent),
                    onClick = {
                        scope.launch { drawerState.close() }
                        navController.navigate(Screen.Downloads.route)
                    },
                    modifier = Modifier.padding(horizontal = 16.dp, vertical = 8.dp)
                )
                
                NavigationDrawerItem(
                    icon = { Icon(Icons.Default.Favorite, contentDescription = null, tint = Color.White) },
                    label = { Text("المكتبة", color = Color.White, fontSize = 16.sp) },
                    selected = currentRoute == Screen.Library.route,
                    colors = NavigationDrawerItemDefaults.colors(unselectedContainerColor = Color.Transparent),
                    onClick = {
                        scope.launch { drawerState.close() }
                        navController.navigate(Screen.Library.route)
                    },
                    modifier = Modifier.padding(horizontal = 16.dp, vertical = 8.dp)
                )

                NavigationDrawerItem(
                    icon = { Icon(Icons.Outlined.Settings, contentDescription = null, tint = Color.White) },
                    label = { Text("الإعدادات", color = Color.White, fontSize = 16.sp) },
                    selected = currentRoute == Screen.Settings.route,
                    colors = NavigationDrawerItemDefaults.colors(unselectedContainerColor = Color.Transparent),
                    onClick = {
                        scope.launch { drawerState.close() }
                        navController.navigate(Screen.Settings.route)
                    },
                    modifier = Modifier.padding(horizontal = 16.dp, vertical = 8.dp)
                )
                
                HorizontalDivider(color = Color(0xFF2A2A2E), modifier = Modifier.padding(horizontal = 24.dp, vertical = 8.dp))
                
                NavigationDrawerItem(
                    icon = { Icon(Icons.Outlined.Info, contentDescription = null, tint = Color.White) },
                    label = { Text("حول التطبيق", color = Color.White, fontSize = 16.sp) },
                    selected = currentRoute == Screen.About.route,
                    colors = NavigationDrawerItemDefaults.colors(unselectedContainerColor = Color.Transparent),
                    onClick = {
                        scope.launch { drawerState.close() }
                        navController.navigate(Screen.About.route)
                    },
                    modifier = Modifier.padding(horizontal = 16.dp, vertical = 8.dp)
                )
                
                NavigationDrawerItem(
                    icon = { Icon(Icons.AutoMirrored.Filled.Help, contentDescription = null, tint = Color.White) },
                    label = { Text("مساعدة ودعم", color = Color.White, fontSize = 16.sp) },
                    selected = false,
                    colors = NavigationDrawerItemDefaults.colors(unselectedContainerColor = Color.Transparent),
                    onClick = { scope.launch { drawerState.close() } },
                    modifier = Modifier.padding(horizontal = 16.dp, vertical = 8.dp)
                )
                
                Spacer(modifier = Modifier.weight(1f))
                
                HorizontalDivider(color = Color(0xFF2A2A2E), modifier = Modifier.padding(horizontal = 24.dp, vertical = 8.dp))

                // Bottom Area (Logout)
                Box(
                    modifier = Modifier
                        .fillMaxWidth()
                        .padding(horizontal = 16.dp, vertical = 16.dp)
                ) {
                    Row(
                        modifier = Modifier
                            .fillMaxWidth()
                            .clip(RoundedCornerShape(12.dp))
                            .border(1.dp, Color(0xFF2A2A2E), RoundedCornerShape(12.dp))
                            .background(Color(0xFF161618))
                            .clickable { 
                                if (isGuest) {
                                    scope.launch { drawerState.close() }
                                    navController.navigate(Screen.Auth.route)
                                } else {
                                    scope.launch { drawerState.close() }
                                    showLogoutDialog = true
                                }
                            }
                            .padding(16.dp),
                        horizontalArrangement = Arrangement.Center,
                        verticalAlignment = Alignment.CenterVertically
                    ) {
                        Text(if (isGuest) "تسجيل الدخول" else "تسجيل الخروج", color = Color.White, fontSize = 16.sp)
                        Spacer(modifier = Modifier.width(12.dp))
                        Icon(if (isGuest) Icons.Default.Person else Icons.AutoMirrored.Filled.ExitToApp, contentDescription = "Log", tint = Color(0xFFE50914))
                    }
                }
            }
        }
    ) {
        androidx.compose.runtime.CompositionLocalProvider(androidx.compose.ui.platform.LocalLayoutDirection provides androidx.compose.ui.unit.LayoutDirection.Ltr) {
        if (showLogoutDialog) {
            AlertDialog(
                onDismissRequest = { showLogoutDialog = false },
                title = { Text("Log Out") },
                text = { Text("Are you sure you want to log out?") },
                confirmButton = {
                    TextButton(onClick = {
                        showLogoutDialog = false
                        scope.launch { userPrefs.saveIsGuest(true) }
                        navController.navigate(Screen.Auth.route) { popUpTo(0) }
                    }) { Text("Yes", color = Color.Red) }
                },
                dismissButton = {
                    TextButton(onClick = { showLogoutDialog = false }) { Text("No", color = Color.White) }
                },
                containerColor = Color(0xFF1E1E20),
                titleContentColor = Color.White,
                textContentColor = Color.LightGray
            )
        }
        Scaffold(
            containerColor = Color.Black,
            topBar = {
                if (bottomBarRoutes.contains(currentRoute) || currentRoute in listOf(Screen.Profile.route, Screen.Downloads.route, Screen.Settings.route, Screen.About.route)) {
                    Column(
                        modifier = Modifier
                            .fillMaxWidth()
                            .windowInsetsPadding(WindowInsets.statusBars)
                    ) {
                        Row(
                            modifier = Modifier
                                .fillMaxWidth()
                                .padding(horizontal = 16.dp, vertical = 12.dp),
                            verticalAlignment = Alignment.CenterVertically
                        ) {
                            // Avatar on left
                            Box(
                                modifier = Modifier
                                    .size(40.dp)
                                    .clip(CircleShape)
                                    .background(Color.DarkGray)
                                    .clickable {
                                         if (isGuest) {
                                            navController.navigate(Screen.Auth.route)
                                        } else {
                                            navController.navigate(Screen.Profile.route)
                                        }
                                    },
                                contentAlignment = Alignment.Center
                            ) {
                                Icon(Icons.Default.Person, contentDescription = "Avatar", tint = Color.LightGray)
                            }
                            Spacer(modifier = Modifier.weight(1f))
                            
                            // Center App Name
                            Text(
                                "CineStream",
                                fontWeight = FontWeight.Bold,
                                color = Color(0xFFE50914), // Red
                                fontSize = 22.sp
                            )
                            
                            Spacer(modifier = Modifier.weight(1f))
                            
                            // Right Icons
                            Icon(Icons.Default.Search, contentDescription = "Search", tint = Color.White, modifier = Modifier.size(24.dp).clickable { isSearchExpanded = !isSearchExpanded })
                            Spacer(modifier = Modifier.width(16.dp))
                            BadgedBox(
                                badge = {
                                    Badge(
                                        containerColor = Color(0xFFE50914), // Red badge
                                        contentColor = Color.White,
                                        modifier = Modifier.offset(x = (-4).dp, y = 4.dp)
                                    ) {
                                        Text("1")
                                    }
                                }
                            ) {
                                Icon(Icons.Outlined.Notifications, contentDescription = "Notifications", tint = Color.White, modifier = Modifier.size(24.dp))
                            }
                            Spacer(modifier = Modifier.width(16.dp))
                            Icon(Icons.Default.Menu, contentDescription = "Menu", tint = Color.White, modifier = Modifier.size(24.dp).clickable { scope.launch { drawerState.open() } })
                        }
                        
                        androidx.compose.animation.AnimatedVisibility(visible = isSearchExpanded) {
                            Column(modifier = Modifier.fillMaxWidth().padding(horizontal = 16.dp)) {
                                TextField(
                                    value = searchQuery,
                                    onValueChange = { searchQuery = it },
                                    placeholder = { Text("Search movies or series...") },
                                    modifier = Modifier.fillMaxWidth(),
                                    colors = TextFieldDefaults.colors(
                                        focusedContainerColor = Color(0xFF1E1E20),
                                        unfocusedContainerColor = Color(0xFF1E1E20),
                                        focusedTextColor = Color.White,
                                        unfocusedTextColor = Color.White,
                                        focusedIndicatorColor = Color.Transparent,
                                        unfocusedIndicatorColor = Color.Transparent
                                    ),
                                    shape = RoundedCornerShape(16.dp),
                                    singleLine = true
                                )
                                if (searchQuery.isNotEmpty()) {
                                    val dummyMovies = listOf("Avatar", "Avengers: Endgame", "Assassin's Creed", "Batman Begins", "Interstellar", "Inception", "Iron Man", "Spider-Man", "Superman")
                                    val searchResults = dummyMovies.filter { it.contains(searchQuery, ignoreCase = true) }
                                    if (searchResults.isNotEmpty()) {
                                        Spacer(modifier = Modifier.height(8.dp))
                                        Card(
                                            colors = CardDefaults.cardColors(containerColor = Color(0xFF2A2A2E)),
                                            modifier = Modifier.fillMaxWidth(),
                                            shape = RoundedCornerShape(16.dp)
                                        ) {
                                            Column(modifier = Modifier.padding(8.dp)) {
                                                searchResults.forEach { result ->
                                                    Text(
                                                        text = result,
                                                        color = Color.White,
                                                        modifier = Modifier
                                                            .fillMaxWidth()
                                                            .clickable { 
                                                                searchQuery = result
                                                                isSearchExpanded = false
                                                            }
                                                            .padding(12.dp)
                                                    )
                                                }
                                            }
                                        }
                                    }
                                }
                            }
                        }
                    }
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
                modifier = Modifier.padding(innerPadding),
                enterTransition = { androidx.compose.animation.fadeIn(animationSpec = androidx.compose.animation.core.tween(300)) },
                exitTransition = { androidx.compose.animation.fadeOut(animationSpec = androidx.compose.animation.core.tween(300)) },
                popEnterTransition = { androidx.compose.animation.fadeIn(animationSpec = androidx.compose.animation.core.tween(300)) },
                popExitTransition = { androidx.compose.animation.fadeOut(animationSpec = androidx.compose.animation.core.tween(300)) }
            ) {
                composable(Screen.Splash.route) {
                    SplashScreen(
                        onNavigateToOnboarding = {
                            navController.navigate(Screen.Onboarding.route) {
                                popUpTo(Screen.Splash.route) { inclusive = true }
                            }
                        },
                        onNavigateToAuth = {
                            navController.navigate(Screen.Auth.route) {
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
                            navController.navigate(Screen.Auth.route) {
                                popUpTo(Screen.Onboarding.route) { inclusive = true }
                            }
                        }
                    )
                }
                composable(Screen.Auth.route) {
                    AuthScreen(
                        onSkip = {
                            navController.navigate(Screen.Home.route) {
                                popUpTo(Screen.Auth.route) { inclusive = true }
                            }
                        },
                        onAuthSuccess = {
                            navController.navigate(Screen.Home.route) {
                                popUpTo(Screen.Auth.route) { inclusive = true }
                            }
                        }
                    )
                }
                composable(Screen.Home.route) {
                    HomeScreen(
                        onMovieClick = { id -> navController.navigate(Screen.MovieDetails.createRoute(id)) },
                        onSeriesClick = { id -> navController.navigate(Screen.SeriesDetails.createRoute(id)) },
                        onNavigateToTrending = { navController.navigate(Screen.Trending.route) },
                        onNavigateToWatching = { navController.navigate(Screen.Watching.route) },
                        onNavigateToPopular = { navController.navigate(Screen.Popular.route) },
                        onNavigateToNewReleases = { navController.navigate(Screen.NewReleases.route) }
                    )
                }
                composable(Screen.Movies.route) {
                    MoviesScreen(
                        onMovieClick = { id -> navController.navigate(Screen.MovieDetails.createRoute(id)) },
                        onNavigateToTrending = { navController.navigate(Screen.Trending.route) },
                        onNavigateToWatching = { navController.navigate(Screen.Watching.route) },
                        onNavigateToPopular = { navController.navigate(Screen.Popular.route) },
                        onNavigateToNewReleases = { navController.navigate(Screen.NewReleases.route) }
                    )
                }
                composable(Screen.Series.route) {
                    SeriesScreen(
                        onSeriesClick = { id -> navController.navigate(Screen.SeriesDetails.createRoute(id)) },
                        onNavigateToTrending = { navController.navigate(Screen.Trending.route) },
                        onNavigateToWatching = { navController.navigate(Screen.Watching.route) },
                        onNavigateToPopular = { navController.navigate(Screen.Popular.route) },
                        onNavigateToNewReleases = { navController.navigate(Screen.NewReleases.route) }
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
                        },
                        onNavigateToTrending = { navController.navigate(Screen.Trending.route) }
                    )
                }
                composable(Screen.Library.route) {
                    LibraryScreen(
                        onItemClick = { id, isMovie ->
                            if (isMovie) {
                                navController.navigate(Screen.MovieDetails.createRoute(id))
                            } else {
                                navController.navigate(Screen.SeriesDetails.createRoute(id))
                            }
                        }
                    )
                }
                composable(Screen.Profile.route) { ProfileScreen() }
                composable(Screen.Downloads.route) { 
                    DownloadsScreen(
                        onItemClick = { id, isMovie ->
                            if (isMovie) {
                                navController.navigate(Screen.MovieDetails.createRoute(id))
                            } else {
                                navController.navigate(Screen.SeriesDetails.createRoute(id))
                            }
                        }
                    ) 
                }
                composable(Screen.Settings.route) { SettingsScreen() }
                composable(Screen.About.route) { AboutScreen() }
                composable(Screen.Trending.route) {
                    TrendingScreen(
                        onItemClick = { id, isMovie ->
                            if (isMovie) {
                                navController.navigate(Screen.MovieDetails.createRoute(id))
                            } else {
                                navController.navigate(Screen.SeriesDetails.createRoute(id))
                            }
                        },
                        onBack = { navController.popBackStack() }
                    )
                }
                composable(Screen.Popular.route) {
                    PopularScreen(
                        onItemClick = { id, isMovie ->
                            if (isMovie) {
                                navController.navigate(Screen.MovieDetails.createRoute(id))
                            } else {
                                navController.navigate(Screen.SeriesDetails.createRoute(id))
                            }
                        },
                        onBack = { navController.popBackStack() }
                    )
                }
                composable(Screen.NewReleases.route) {
                    NewReleasesScreen(
                        onItemClick = { id, isMovie ->
                            if (isMovie) {
                                navController.navigate(Screen.MovieDetails.createRoute(id))
                            } else {
                                navController.navigate(Screen.SeriesDetails.createRoute(id))
                            }
                        },
                        onBack = { navController.popBackStack() }
                    )
                }
                composable(Screen.Watching.route) {
                    WatchingScreen(
                        onItemClick = { id, isMovie ->
                            if (isMovie) {
                                navController.navigate(Screen.MovieDetails.createRoute(id))
                            } else {
                                navController.navigate(Screen.SeriesDetails.createRoute(id))
                            }
                        },
                        onBack = { navController.popBackStack() }
                    )
                }
                composable(Screen.MovieDetails.route) { backStackEntry ->
                    val movieId = backStackEntry.arguments?.getString("movieId") ?: return@composable
                    MovieDetailsScreen(
                        movieId = movieId, 
                        onBack = { navController.popBackStack() },
                        onPlay = { url -> 
                            val encodedUrl = URLEncoder.encode(url, "UTF-8")
                            navController.navigate("player?url=$encodedUrl")
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
                            navController.navigate("player?url=$encodedUrl")
                        }
                    )
                }
                composable("player?url={url}") { backStackEntry ->
                    val url = backStackEntry.arguments?.getString("url") ?: return@composable
                    val decodedUrl = URLDecoder.decode(url, "UTF-8")
                    PlayerScreen(videoUrl = decodedUrl, onBack = { navController.popBackStack() })
                }
            }
        }
    }
}
}
}
// Trending and Watching added at the end using sed later
