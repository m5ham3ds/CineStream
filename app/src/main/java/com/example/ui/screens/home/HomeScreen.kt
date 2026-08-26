package com.example.ui.screens.home

import androidx.compose.foundation.background
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.lazy.LazyRow
import androidx.compose.foundation.lazy.items
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.verticalScroll
import androidx.compose.material3.*
import androidx.compose.runtime.Composable
import androidx.compose.runtime.collectAsState
import androidx.compose.runtime.getValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Brush
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.layout.ContentScale
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import androidx.lifecycle.viewmodel.compose.viewModel
import coil.compose.AsyncImage
import com.example.domain.models.Movie
import com.example.domain.models.Series
import com.example.ui.ViewModelFactory
import com.example.ui.components.MediaCard

@Composable
fun HomeScreen(
    onMovieClick: (String) -> Unit,
    onSeriesClick: (String) -> Unit,
    viewModel: HomeViewModel = viewModel(factory = ViewModelFactory())
) {
    val uiState by viewModel.uiState.collectAsState()

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
                    onClick = { onMovieClick(movie.id) }
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
                    onClick = { onSeriesClick(series.id) }
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
                    onClick = { onMovieClick(movie.id) }
                )
            }
        }
    }
}

@Composable
fun HeroSection(movie: Movie, onClick: () -> Unit) {
    Box(
        modifier = Modifier
            .fillMaxWidth()
            .aspectRatio(16f / 9f)
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
                        colors = listOf(Color.Transparent, MaterialTheme.colorScheme.background),
                        startY = 50f
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
                fontWeight = FontWeight.Bold
            )
            Spacer(modifier = Modifier.height(4.dp))
            Row(horizontalArrangement = Arrangement.spacedBy(8.dp)) {
                movie.genres.take(3).forEach { genre ->
                    Text(text = genre, style = MaterialTheme.typography.bodySmall, color = Color.Gray)
                }
            }
            Spacer(modifier = Modifier.height(8.dp))
            Button(onClick = onClick) {
                Text("Play")
            }
        }
    }
}

@Composable
fun SectionTitle(title: String) {
    Text(
        text = title,
        style = MaterialTheme.typography.titleMedium,
        fontWeight = FontWeight.Bold,
        modifier = Modifier.padding(horizontal = 16.dp, vertical = 8.dp)
    )
}
