package com.example.ui.screens.details

import androidx.compose.foundation.background
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.verticalScroll
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.automirrored.filled.ArrowBack
import androidx.compose.material.icons.filled.Download
import androidx.compose.material.icons.filled.FavoriteBorder
import androidx.compose.material.icons.filled.PlayArrow
import androidx.compose.material3.*
import androidx.compose.runtime.Composable
import androidx.compose.runtime.LaunchedEffect
import androidx.compose.runtime.collectAsState
import androidx.compose.runtime.getValue
import androidx.compose.runtime.setValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
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
import java.net.URLEncoder
import androidx.navigation.NavController
import androidx.navigation.compose.rememberNavController
import com.example.ui.components.DownloadQualitySheet
import androidx.compose.foundation.shape.CircleShape
import androidx.compose.ui.platform.LocalContext
import android.widget.Toast
import com.example.data.repository.DownloadRepository
import com.example.data.model.DownloadItem
import com.example.data.repository.LibraryRepository
import com.example.data.model.LibraryItem
import kotlinx.coroutines.launch
import androidx.compose.runtime.rememberCoroutineScope

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun MovieDetailsScreen(
    movieId: String, 
    onBack: () -> Unit,
    onPlay: (String) -> Unit,
    viewModel: MovieDetailsViewModel = viewModel(factory = ViewModelFactory())
) {
    val uiState by viewModel.uiState.collectAsState()
    val defaultVideoUrl = "https://test-streams.mux.dev/x36xhzz/x36xhzz.m3u8"
    val context = LocalContext.current
    val downloadRepository = remember { DownloadRepository(context) }
    val libraryRepository = remember { LibraryRepository(context) }
    val scope = rememberCoroutineScope()

    LaunchedEffect(movieId) {
        viewModel.loadMovie(movieId)
    }

    Scaffold(
        topBar = {
            TopAppBar(
                title = { Text("") },
                navigationIcon = {
                    IconButton(onClick = onBack) {
                        Icon(Icons.AutoMirrored.Filled.ArrowBack, contentDescription = "Back", tint = Color.White)
                    }
                },
                colors = TopAppBarDefaults.topAppBarColors(
                    containerColor = Color.Transparent,
                    navigationIconContentColor = Color.White
                )
            )
        }
    ) { padding ->
        if (uiState.isLoading) {
            Box(modifier = Modifier.fillMaxSize(), contentAlignment = Alignment.Center) {
                CircularProgressIndicator()
            }
        } else if (uiState.error != null) {
            Box(modifier = Modifier.fillMaxSize(), contentAlignment = Alignment.Center) {
                Text(uiState.error ?: "Error loading movie")
            }
        } else if (uiState.movie != null) {
            val movie = uiState.movie!!
            Column(
                modifier = Modifier
                    .fillMaxSize()
                    .verticalScroll(rememberScrollState())
            ) {
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
                }

                Column(modifier = Modifier.padding(16.dp)) {
                    Text(
                        text = movie.title,
                        style = MaterialTheme.typography.headlineLarge,
                        fontWeight = FontWeight.Bold
                    )
                    Spacer(modifier = Modifier.height(8.dp))
                    Row(
                        horizontalArrangement = Arrangement.spacedBy(16.dp),
                        verticalAlignment = Alignment.CenterVertically
                    ) {
                        Text(text = "${movie.year}", style = MaterialTheme.typography.bodyMedium)
                        Text(text = "${movie.rating} ★", style = MaterialTheme.typography.bodyMedium, color = Color.Yellow)
                        Text(text = "${movie.runtime} min", style = MaterialTheme.typography.bodyMedium)
                    }
                    Spacer(modifier = Modifier.height(16.dp))
                    var showDownloadSheet by remember { mutableStateOf(false) }

                    Row(
                        modifier = Modifier.fillMaxWidth(),
                        horizontalArrangement = Arrangement.spacedBy(16.dp),
                        verticalAlignment = Alignment.CenterVertically
                    ) {
                        Button(
                            onClick = { onPlay(defaultVideoUrl) },
                            modifier = Modifier.weight(1f)
                        ) {
                            Icon(Icons.Default.PlayArrow, contentDescription = "Play")
                            Spacer(modifier = Modifier.width(8.dp))
                            Text("Watch Now")
                        }

                        IconButton(
                            onClick = { showDownloadSheet = true },
                            modifier = Modifier.background(MaterialTheme.colorScheme.surfaceVariant, shape = CircleShape)
                        ) {
                            Icon(Icons.Default.Download, contentDescription = "Download")
                        }

                        IconButton(
                            onClick = { 
                                uiState.movie?.let { movie ->
                                    scope.launch {
                                        libraryRepository.addToLibrary(LibraryItem(
                                            id = movie.id, title = movie.title, posterUrl = movie.posterUrl, isMovie = true
                                        ))
                                        Toast.makeText(context, "Added to Library", Toast.LENGTH_SHORT).show()
                                    }
                                }
                            },
                            modifier = Modifier.background(MaterialTheme.colorScheme.surfaceVariant, shape = CircleShape)
                        ) {
                            Icon(Icons.Default.FavoriteBorder, contentDescription = "Add to List")
                        }
                    }

                    if (showDownloadSheet) {
                        DownloadQualitySheet(
                            onDismiss = { showDownloadSheet = false },
                            onQualitySelected = { quality ->
                                uiState.movie?.let { movie ->
                                    scope.launch {
                                        downloadRepository.addToDownloads(DownloadItem(
                                            id = movie.id, title = movie.title, posterUrl = movie.posterUrl, isMovie = true, quality = quality
                                        ))
                                        Toast.makeText(context, "Download Started", Toast.LENGTH_SHORT).show()
                                        showDownloadSheet = false
                                    }
                                }
                            }
                        )
                    }
                    Spacer(modifier = Modifier.height(16.dp))
                    Text(text = movie.overview, style = MaterialTheme.typography.bodyLarge)
                    Spacer(modifier = Modifier.height(16.dp))
                    Text(text = "Genres: ${movie.genres.joinToString(", ")}", style = MaterialTheme.typography.bodyMedium, color = Color.Gray)
                    Text(text = "Cast: ${movie.cast.joinToString(", ")}", style = MaterialTheme.typography.bodyMedium, color = Color.Gray)
                }
            }
        }
    }
}

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun SeriesDetailsScreen(
    seriesId: String, 
    onBack: () -> Unit,
    onPlay: (String) -> Unit,
    viewModel: SeriesDetailsViewModel = viewModel(factory = ViewModelFactory())
) {
    val uiState by viewModel.uiState.collectAsState()
    val defaultVideoUrl = "https://test-streams.mux.dev/x36xhzz/x36xhzz.m3u8"
    val context = LocalContext.current
    val downloadRepository = remember { DownloadRepository(context) }
    val libraryRepository = remember { LibraryRepository(context) }
    val scope = rememberCoroutineScope()

    LaunchedEffect(seriesId) {
        viewModel.loadSeries(seriesId)
    }

    Scaffold(
        topBar = {
            TopAppBar(
                title = { Text("") },
                navigationIcon = {
                    IconButton(onClick = onBack) {
                        Icon(Icons.AutoMirrored.Filled.ArrowBack, contentDescription = "Back", tint = Color.White)
                    }
                },
                colors = TopAppBarDefaults.topAppBarColors(
                    containerColor = Color.Transparent,
                    navigationIconContentColor = Color.White
                )
            )
        }
    ) { padding ->
        if (uiState.isLoading) {
            Box(modifier = Modifier.fillMaxSize(), contentAlignment = Alignment.Center) {
                CircularProgressIndicator()
            }
        } else if (uiState.error != null) {
            Box(modifier = Modifier.fillMaxSize(), contentAlignment = Alignment.Center) {
                Text(uiState.error ?: "Error loading series")
            }
        } else if (uiState.series != null) {
            val series = uiState.series!!
            Column(
                modifier = Modifier
                    .fillMaxSize()
                    .verticalScroll(rememberScrollState())
            ) {
                Box(
                    modifier = Modifier
                        .fillMaxWidth()
                        .aspectRatio(16f / 9f)
                ) {
                    AsyncImage(
                        model = series.backdropUrl,
                        contentDescription = series.title,
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
                }

                Column(modifier = Modifier.padding(16.dp)) {
                    Text(
                        text = series.title,
                        style = MaterialTheme.typography.headlineLarge,
                        fontWeight = FontWeight.Bold
                    )
                    Spacer(modifier = Modifier.height(8.dp))
                    Row(
                        horizontalArrangement = Arrangement.spacedBy(16.dp),
                        verticalAlignment = Alignment.CenterVertically
                    ) {
                        Text(text = "${series.year}", style = MaterialTheme.typography.bodyMedium)
                        Text(text = "${series.rating} ★", style = MaterialTheme.typography.bodyMedium, color = Color.Yellow)
                        Text(text = "${series.seasons.size} Seasons", style = MaterialTheme.typography.bodyMedium)
                    }
                    Spacer(modifier = Modifier.height(16.dp))
                    var showDownloadSheet by remember { mutableStateOf(false) }

                    Row(
                        modifier = Modifier.fillMaxWidth(),
                        horizontalArrangement = Arrangement.spacedBy(16.dp),
                        verticalAlignment = Alignment.CenterVertically
                    ) {
                        Button(
                            onClick = { onPlay(defaultVideoUrl) },
                            modifier = Modifier.weight(1f)
                        ) {
                            Icon(Icons.Default.PlayArrow, contentDescription = "Play")
                            Spacer(modifier = Modifier.width(8.dp))
                            Text("Resume")
                        }

                        IconButton(
                            onClick = { showDownloadSheet = true },
                            modifier = Modifier.background(MaterialTheme.colorScheme.surfaceVariant, shape = CircleShape)
                        ) {
                            Icon(Icons.Default.Download, contentDescription = "Download")
                        }

                        IconButton(
                            onClick = { 
                                uiState.series?.let { series ->
                                    scope.launch {
                                        libraryRepository.addToLibrary(LibraryItem(
                                            id = series.id, title = series.title, posterUrl = series.posterUrl, isMovie = false
                                        ))
                                        Toast.makeText(context, "Added to Library", Toast.LENGTH_SHORT).show()
                                    }
                                }
                            },
                            modifier = Modifier.background(MaterialTheme.colorScheme.surfaceVariant, shape = CircleShape)
                        ) {
                            Icon(Icons.Default.FavoriteBorder, contentDescription = "Add to List")
                        }
                    }

                    if (showDownloadSheet) {
                        DownloadQualitySheet(
                            onDismiss = { showDownloadSheet = false },
                            onQualitySelected = { quality ->
                                uiState.series?.let { series ->
                                    scope.launch {
                                        downloadRepository.addToDownloads(DownloadItem(
                                            id = series.id, title = series.title, posterUrl = series.posterUrl, isMovie = false, quality = quality
                                        ))
                                        Toast.makeText(context, "Download Started", Toast.LENGTH_SHORT).show()
                                        showDownloadSheet = false
                                    }
                                }
                            }
                        )
                    }
                    Spacer(modifier = Modifier.height(16.dp))
                    Text(text = series.overview, style = MaterialTheme.typography.bodyLarge)
                    Spacer(modifier = Modifier.height(16.dp))
                    Text(text = "Genres: ${series.genres.joinToString(", ")}", style = MaterialTheme.typography.bodyMedium, color = Color.Gray)
                    
                    Spacer(modifier = Modifier.height(24.dp))
                    Text(text = "Seasons", style = MaterialTheme.typography.titleLarge, fontWeight = FontWeight.Bold)
                    Spacer(modifier = Modifier.height(8.dp))
                    series.seasons.forEach { season ->
                        Card(
                            modifier = Modifier
                                .fillMaxWidth()
                                .padding(vertical = 4.dp),
                            colors = CardDefaults.cardColors(containerColor = MaterialTheme.colorScheme.surfaceVariant)
                        ) {
                            Text(
                                text = season.title,
                                modifier = Modifier.padding(16.dp),
                                style = MaterialTheme.typography.bodyLarge
                            )
                        }
                    }
                }
            }
        }
    }
}
