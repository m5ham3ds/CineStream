package com.example.ui.screens.home

import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.ui.draw.clip
import androidx.compose.foundation.background
import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.lazy.LazyRow
import androidx.compose.foundation.lazy.items
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.verticalScroll
import androidx.compose.material3.*
import androidx.compose.runtime.Composable
import androidx.compose.runtime.collectAsState
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.setValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Brush
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.layout.ContentScale
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import androidx.lifecycle.viewmodel.compose.viewModel
import android.widget.Toast
import androidx.compose.ui.platform.LocalContext
import coil.compose.AsyncImage
import com.example.domain.models.Movie
import com.example.domain.models.Series
import com.example.ui.ViewModelFactory
import com.example.ui.components.MediaCard
import com.example.ui.components.MediaActionBottomSheet
import com.example.data.repository.LibraryRepository
import com.example.data.model.LibraryItem
import com.example.data.repository.DownloadRepository
import com.example.data.model.DownloadItem
import kotlinx.coroutines.launch
import androidx.compose.runtime.rememberCoroutineScope

@Composable
fun HomeScreen(
    onMovieClick: (String) -> Unit,
    onSeriesClick: (String) -> Unit,
    viewModel: HomeViewModel = viewModel(factory = ViewModelFactory())
) {
    val uiState by viewModel.uiState.collectAsState()
    val context = LocalContext.current
    val libraryRepository = remember { LibraryRepository(context) }
    val downloadRepository = remember { DownloadRepository(context) }
    val scope = rememberCoroutineScope()

    if (uiState.isLoading) {
        Box(modifier = Modifier.fillMaxSize(), contentAlignment = Alignment.Center) {
            CircularProgressIndicator()
        }
        return
    }

    if (uiState.error != null) {
        Box(modifier = Modifier.fillMaxSize(), contentAlignment = Alignment.Center) {
            Text(text = uiState.error ?: "Unknown error")
        }
        return
    }

    val scrollState = rememberScrollState()
    var showBottomSheet by remember { mutableStateOf(false) }
    var bottomSheetIsMovie by remember { mutableStateOf(true) }
    var selectedMediaId by remember { mutableStateOf("") }
    var selectedMediaTitle by remember { mutableStateOf("") }
    var selectedMediaPoster by remember { mutableStateOf("") }

    Column(
        modifier = Modifier
            .fillMaxSize()
            .verticalScroll(scrollState)
            .padding(bottom = 80.dp)
    ) {
        val heroMovie = uiState.trendingMovies.firstOrNull()
        if (heroMovie != null) {
            HeroSection(movie = heroMovie, onClick = { onMovieClick(heroMovie.id) })
        }

        Spacer(modifier = Modifier.height(24.dp))

        SectionTitle("Trending Movies")
        LazyRow(
            contentPadding = PaddingValues(horizontal = 16.dp),
            horizontalArrangement = Arrangement.spacedBy(16.dp)
        ) {
            items(uiState.trendingMovies) { movie ->
                MediaCard(
                    title = movie.title,
                    posterUrl = movie.posterUrl,
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

        SectionTitle("Trending Series")
        LazyRow(
            contentPadding = PaddingValues(horizontal = 16.dp),
            horizontalArrangement = Arrangement.spacedBy(16.dp)
        ) {
            items(uiState.trendingSeries) { series ->
                MediaCard(
                    title = series.title,
                    posterUrl = series.posterUrl,
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

        Spacer(modifier = Modifier.height(24.dp))

        SectionTitle("Action Movies")
        LazyRow(
            contentPadding = PaddingValues(horizontal = 16.dp),
            horizontalArrangement = Arrangement.spacedBy(16.dp)
        ) {
            items(uiState.actionMovies) { movie ->
                MediaCard(
                    title = movie.title,
                    posterUrl = movie.posterUrl,
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

@Composable
fun HeroSection(movie: Movie, onClick: () -> Unit) {
    Box(
        modifier = Modifier
            .fillMaxWidth()
            .padding(horizontal = 16.dp, vertical = 8.dp)
            .aspectRatio(16f / 9f)
            .clip(RoundedCornerShape(16.dp))
    ) {
        AsyncImage(
            model = movie.backdropUrl,
            contentDescription = movie.title,
            contentScale = ContentScale.Crop,
            modifier = Modifier.fillMaxSize()
        )
        Box(
            modifier = Modifier
                .fillMaxSize()
                .background(
                    Brush.verticalGradient(
                        colors = listOf(Color.Transparent, Color.Black.copy(alpha = 0.8f)),
                        startY = 100f
                    )
                )
        )
        Column(
            modifier = Modifier
                .align(Alignment.BottomStart)
                .padding(16.dp)
        ) {
            Text(
                text = movie.title,
                style = MaterialTheme.typography.headlineMedium,
                fontWeight = FontWeight.Bold,
                color = Color.White
            )
            Spacer(modifier = Modifier.height(12.dp))
            Box(
                modifier = Modifier
                    .clip(RoundedCornerShape(percent = 50))
                    .background(Color.White.copy(alpha = 0.2f))
                    .clickable { onClick() }
                    .padding(horizontal = 24.dp, vertical = 8.dp),
                contentAlignment = Alignment.Center
            ) {
                Text("Play", color = Color.White, fontWeight = FontWeight.Normal)
            }
        }
    }
}

@Composable
fun SectionTitle(title: String) {
    Text(
        text = title,
        style = MaterialTheme.typography.titleMedium,
        fontWeight = FontWeight.SemiBold,
        color = Color.White,
        modifier = Modifier.padding(horizontal = 16.dp, vertical = 12.dp)
    )
}
