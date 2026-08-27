package com.example.ui.screens.home

import android.widget.Toast
import androidx.compose.foundation.background
import androidx.compose.foundation.border
import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.lazy.LazyRow
import androidx.compose.foundation.lazy.items
import androidx.compose.foundation.lazy.itemsIndexed
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.shape.CircleShape
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.foundation.verticalScroll
import androidx.compose.foundation.pager.*
import kotlinx.coroutines.delay
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.Add
import androidx.compose.material.icons.filled.PlayArrow
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.graphics.Brush
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.layout.ContentScale
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import androidx.lifecycle.viewmodel.compose.viewModel
import coil.compose.AsyncImage
import com.example.data.model.DownloadItem
import com.example.data.model.LibraryItem
import com.example.data.repository.DownloadRepository
import com.example.data.repository.LibraryRepository
import com.example.domain.models.Movie
import com.example.ui.ViewModelFactory
import com.example.ui.components.MediaActionBottomSheet
import com.example.ui.components.MediaCard
import kotlinx.coroutines.launch

@Composable
fun HomeScreen(
    onMovieClick: (String) -> Unit,
    onSeriesClick: (String) -> Unit,
    onNavigateToTrending: () -> Unit = {},
    onNavigateToWatching: () -> Unit = {},
    viewModel: HomeViewModel = viewModel(factory = ViewModelFactory())
) {
    val uiState by viewModel.uiState.collectAsState()
    val context = LocalContext.current
    val libraryRepository = remember { LibraryRepository(context) }
    val downloadRepository = remember { DownloadRepository(context) }
    val scope = rememberCoroutineScope()

    if (uiState.isLoading) {
        Box(modifier = Modifier.fillMaxSize(), contentAlignment = Alignment.Center) {
            CircularProgressIndicator(color = Color(0xFFE50914))
        }
        return
    }

    if (uiState.error != null) {
        Box(modifier = Modifier.fillMaxSize(), contentAlignment = Alignment.Center) {
            Text(text = uiState.error ?: "Unknown error", color = Color.White)
        }
        return
    }

    val scrollState = rememberScrollState()
    var showBottomSheet by remember { mutableStateOf(false) }
    var bottomSheetIsMovie by remember { mutableStateOf(true) }
    var selectedMediaId by remember { mutableStateOf("") }
    var selectedMediaTitle by remember { mutableStateOf("") }
    var selectedMediaPoster by remember { mutableStateOf("") }

    var selectedCategory by remember { mutableStateOf("Home") }
    val categories = listOf("Home", "Movies", "Series", "Anime", "Documentaries")

    Column(
        modifier = Modifier
            .fillMaxSize()
            .verticalScroll(scrollState)
             // Leave space for bottom nav
    ) {
        // Categories Tab Row
        LazyRow(
            modifier = Modifier.fillMaxWidth().padding(horizontal = 16.dp, vertical = 8.dp),
            horizontalArrangement = Arrangement.spacedBy(8.dp)
        ) {
            items(categories) { category ->
                Box(
                    modifier = Modifier
                        .clip(RoundedCornerShape(8.dp))
                        .background(if (selectedCategory == category) Color(0xFFE50914) else Color(0xFF1E1E20))
                        .border(
                            width = 1.dp,
                            color = if (selectedCategory == category) Color.Transparent else Color.DarkGray,
                            shape = RoundedCornerShape(8.dp)
                        )
                        .clickable { selectedCategory = category }
                        .padding(horizontal = 16.dp, vertical = 8.dp),
                    contentAlignment = Alignment.Center
                ) {
                    Text(
                        text = category,
                        color = Color.White,
                        fontSize = 14.sp,
                        fontWeight = if (selectedCategory == category) FontWeight.SemiBold else FontWeight.Normal
                    )
                }
            }
        }

        // Hero Section
        if (uiState.trendingMovies.isNotEmpty()) {
            HeroCarousel(movies = uiState.trendingMovies.take(5), onClick = onMovieClick)
        }

        Spacer(modifier = Modifier.height(24.dp))

        // Trending Now
        SectionTitle("Trending Now", onSeeAllClick = onNavigateToTrending)
        LazyRow(
            contentPadding = PaddingValues(horizontal = 16.dp),
            horizontalArrangement = Arrangement.spacedBy(16.dp)
        ) {
            itemsIndexed(uiState.trendingMovies) { index, movie ->
                MediaCard(
                    title = movie.title,
                    posterUrl = movie.posterUrl,
                    rank = index + 1,
                    rating = 8.0 + (index * 0.1),
                    year = "2024",
                    onClick = { onMovieClick(movie.id) },
                    onLongClick = { 
                        bottomSheetIsMovie = true
                        selectedMediaId = movie.id
                        selectedMediaTitle = movie.title
                        selectedMediaPoster = movie.posterUrl
                        showBottomSheet = true
                    }
                )
            }
        }

        Spacer(modifier = Modifier.height(24.dp))
        
        // Continue Watching (Demo Item)
        SectionTitle("Continue Watching", onSeeAllClick = onNavigateToWatching)
        ContinueWatchingCard()

        Spacer(modifier = Modifier.height(24.dp))

        // Trending Series
        SectionTitle("Trending Series", onSeeAllClick = onNavigateToTrending)
        LazyRow(
            contentPadding = PaddingValues(horizontal = 16.dp),
            horizontalArrangement = Arrangement.spacedBy(16.dp)
        ) {
            itemsIndexed(uiState.trendingSeries) { index, series ->
                MediaCard(
                    title = series.title,
                    posterUrl = series.posterUrl,
                    rank = index + 1,
                    rating = 8.5 + (index * 0.1),
                    year = "${series.seasons.size} Seasons",
                    isMovie = false,
                    onClick = { onSeriesClick(series.id) },
                    onLongClick = { 
                        bottomSheetIsMovie = false
                        selectedMediaId = series.id
                        selectedMediaTitle = series.title
                        selectedMediaPoster = series.posterUrl
                        showBottomSheet = true
                    }
                )
            }
        }

        if (showBottomSheet) {
            MediaActionBottomSheet(
                isMovie = bottomSheetIsMovie,
                onDismissRequest = { showBottomSheet = false },
                onDownloadStart = { quality ->
                    scope.launch {
                        downloadRepository.addToDownloads(DownloadItem(
                            id = selectedMediaId,
                            title = selectedMediaTitle,
                            posterUrl = selectedMediaPoster,
                            isMovie = bottomSheetIsMovie,
                            quality = quality
                        ))
                        Toast.makeText(context, "Download Started", Toast.LENGTH_SHORT).show()
                    }
                },
                onAddToLibrary = {
                    scope.launch {
                        libraryRepository.addToLibrary(LibraryItem(
                            id = selectedMediaId,
                            title = selectedMediaTitle,
                            posterUrl = selectedMediaPoster,
                            isMovie = bottomSheetIsMovie
                        ))
                        Toast.makeText(context, "Added to Library", Toast.LENGTH_SHORT).show()
                    }
                }
            )
        }
    }
}

@OptIn(androidx.compose.foundation.ExperimentalFoundationApi::class)
@Composable
fun HeroCarousel(movies: List<Movie>, onClick: (String) -> Unit) {
    val pagerState = rememberPagerState(pageCount = { movies.size })

    LaunchedEffect(pagerState) {
        while (true) {
            delay(3000)
            val nextPage = (pagerState.currentPage + 1) % movies.size
            pagerState.animateScrollToPage(nextPage)
        }
    }

    Box(
        modifier = Modifier
            .fillMaxWidth()
            .padding(horizontal = 16.dp)
            .aspectRatio(16f / 10f)
            .clip(RoundedCornerShape(16.dp))
    ) {
        HorizontalPager(state = pagerState) { page ->
            val movie = movies[page]
            Box(modifier = Modifier.fillMaxSize()) {
                AsyncImage(
                    model = movie.backdropUrl,
                    contentDescription = movie.title,
                    contentScale = ContentScale.Crop,
                    modifier = Modifier.fillMaxSize()
                )
                // Background Gradient
                Box(
                    modifier = Modifier
                        .fillMaxSize()
                        .background(
                            Brush.verticalGradient(
                                colors = listOf(Color.Transparent, Color.Black.copy(alpha = 0.9f)),
                                startY = 100f
                            )
                        )
                )
                
                Column(
                    modifier = Modifier
                        .align(Alignment.BottomStart)
                        .padding(16.dp)
                ) {
                    Box(
                        modifier = Modifier
                            .background(Color.White.copy(alpha = 0.2f), RoundedCornerShape(4.dp))
                            .padding(horizontal = 8.dp, vertical = 4.dp)
                    ) {
                        Text("NEW RELEASE", color = Color.White, fontSize = 10.sp, fontWeight = FontWeight.Bold)
                    }
                    Spacer(modifier = Modifier.height(8.dp))
                    Text(
                        text = movie.title,
                        style = MaterialTheme.typography.headlineLarge,
                        fontWeight = FontWeight.Bold,
                        color = Color.White
                    )
                    Spacer(modifier = Modifier.height(4.dp))
                    Text(
                        text = "An unforgettable journey\ninto the wild",
                        color = Color.LightGray,
                        fontSize = 12.sp,
                        lineHeight = 16.sp
                    )
                    Spacer(modifier = Modifier.height(16.dp))
                    Row(verticalAlignment = Alignment.CenterVertically) {
                        Box(
                            modifier = Modifier
                                .clip(RoundedCornerShape(percent = 50))
                                .background(Color(0xFFE50914))
                                .clickable { onClick(movie.id) }
                                .padding(horizontal = 24.dp, vertical = 10.dp),
                            contentAlignment = Alignment.Center
                        ) {
                            Row(verticalAlignment = Alignment.CenterVertically) {
                                Icon(Icons.Default.PlayArrow, contentDescription = "Play", tint = Color.White, modifier = Modifier.size(16.dp))
                                Spacer(modifier = Modifier.width(4.dp))
                                Text("Play", color = Color.White, fontWeight = FontWeight.SemiBold)
                            }
                        }
                        Spacer(modifier = Modifier.width(12.dp))
                        Box(
                            modifier = Modifier
                                .size(40.dp)
                                .clip(CircleShape)
                                .border(1.dp, Color.White, CircleShape)
                                .clickable { /* Add to list */ },
                            contentAlignment = Alignment.Center
                        ) {
                            Icon(Icons.Default.Add, contentDescription = "Add", tint = Color.White)
                        }
                    }
                }
            }
        }
        
        // Carousel Dots
        Row(
            modifier = Modifier
                .align(Alignment.BottomEnd)
                .padding(16.dp),
            horizontalArrangement = Arrangement.spacedBy(4.dp)
        ) {
            repeat(movies.size) { index ->
                val isSelected = pagerState.currentPage == index
                Box(
                    modifier = Modifier
                        .size(if (isSelected) 16.dp else 4.dp, 4.dp)
                        .clip(RoundedCornerShape(2.dp))
                        .background(if (isSelected) Color(0xFFE50914) else Color.Gray)
                )
            }
        }
    }
}

@Composable
fun SectionTitle(title: String, onSeeAllClick: (() -> Unit)? = null) {
    Row(
        modifier = Modifier.fillMaxWidth().padding(horizontal = 16.dp, vertical = 12.dp),
        horizontalArrangement = Arrangement.SpaceBetween,
        verticalAlignment = Alignment.CenterVertically
    ) {
        Text(
            text = title,
            style = MaterialTheme.typography.titleMedium,
            fontWeight = FontWeight.Bold,
            color = Color.White
        )
        if (onSeeAllClick != null) {
            Text(
                text = "See All",
                style = MaterialTheme.typography.labelLarge,
                color = Color(0xFFE50914),
                modifier = Modifier.clickable { onSeeAllClick() }
            )
        }
    }
}

@Composable
fun ContinueWatchingCard() {
    Box(
        modifier = Modifier
            .fillMaxWidth()
            .padding(horizontal = 16.dp)
            .clip(RoundedCornerShape(12.dp))
            .background(Color(0xFF1E1E20))
            .clickable { /* Resume */ }
    ) {
        Row(
            modifier = Modifier.fillMaxWidth(),
            verticalAlignment = Alignment.CenterVertically
        ) {
            Box(modifier = Modifier.width(120.dp).height(80.dp)) {
                AsyncImage(
                    model = "https://image.tmdb.org/t/p/w500/8Y43POKjjKDGI9MH89NW0NAzzp8.jpg", // Placeholder
                    contentDescription = "Continue Watching",
                    contentScale = ContentScale.Crop,
                    modifier = Modifier.fillMaxSize()
                )
                // Red progress bar at bottom of image
                Box(modifier = Modifier.align(Alignment.BottomStart).fillMaxWidth().height(3.dp).background(Color.DarkGray)) {
                    Box(modifier = Modifier.fillMaxWidth(0.6f).height(3.dp).background(Color(0xFFE50914)))
                }
            }
            
            Column(
                modifier = Modifier
                    .weight(1f)
                    .padding(horizontal = 12.dp)
            ) {
                Text("Demo Series 01", color = Color.White, fontWeight = FontWeight.SemiBold, fontSize = 14.sp)
                Spacer(modifier = Modifier.height(4.dp))
                Text("S1 • E3", color = Color.Gray, fontSize = 12.sp)
                Spacer(modifier = Modifier.height(2.dp))
                Text("24m left", color = Color.Gray, fontSize = 12.sp)
            }
            
            Box(
                modifier = Modifier
                    .padding(end = 16.dp)
                    .size(36.dp)
                    .clip(CircleShape)
                    .background(Color.White.copy(alpha = 0.1f)),
                contentAlignment = Alignment.Center
            ) {
                Icon(Icons.Default.PlayArrow, contentDescription = "Play", tint = Color.White, modifier = Modifier.size(20.dp))
            }
            
            Text("⋮", color = Color.Gray, fontSize = 24.sp, modifier = Modifier.padding(end = 12.dp).clickable { /* Options */ })
        }
    }
}
