package com.example.ui.screens.series

import android.widget.Toast
import androidx.compose.foundation.background
import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.lazy.LazyRow
import androidx.compose.foundation.lazy.items
import androidx.compose.foundation.lazy.itemsIndexed
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.foundation.verticalScroll
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.ArrowDropDown
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import androidx.lifecycle.viewmodel.compose.viewModel
import com.example.data.model.DownloadItem
import com.example.data.model.LibraryItem
import com.example.data.repository.DownloadRepository
import com.example.data.repository.LibraryRepository
import com.example.ui.ViewModelFactory
import com.example.ui.components.ContinueWatchingCardShared
import com.example.ui.components.HeroSectionShared
import com.example.ui.components.MediaActionBottomSheet
import com.example.ui.components.MediaCard
import com.example.ui.components.SectionTitleShared
import kotlinx.coroutines.launch

@Composable
fun SeriesScreen(
    onSeriesClick: (String) -> Unit,
    onNavigateToTrending: () -> Unit = {},
    onNavigateToWatching: () -> Unit = {},
    onNavigateToPopular: () -> Unit = {},
    onNavigateToNewReleases: () -> Unit = {},
    viewModel: SeriesViewModel = viewModel(factory = ViewModelFactory())
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
    var selectedMediaId by remember { mutableStateOf("") }
    var selectedMediaTitle by remember { mutableStateOf("") }
    var selectedMediaPoster by remember { mutableStateOf("") }

    var selectedCategory by remember { mutableStateOf("All") }
    val categories = listOf("All", "Trending", "New Releases", "Top Rated", "Genres")

    Column(
        modifier = Modifier
            .fillMaxSize()
            .verticalScroll(scrollState)
            
    ) {
        Text(
            text = "Series",
            style = MaterialTheme.typography.headlineMedium,
            fontWeight = FontWeight.Bold,
            color = Color.White,
            modifier = Modifier.padding(horizontal = 16.dp, vertical = 8.dp)
        )

        // Hero Section
        val heroSeries = uiState.series.firstOrNull()
        if (heroSeries != null) {
            HeroSectionShared(
                title = "Demo Series 01", 
                backdropUrl = heroSeries.backdropUrl, 
                desc = "A journey of power, betrayal and\ndestiny.", 
                tag = "TRENDING NOW",
                onClick = { onSeriesClick(heroSeries.id) }
            )
        }


        Spacer(modifier = Modifier.height(16.dp))
        // Categories Tab Row
        LazyRow(
            modifier = Modifier.fillMaxWidth().padding(horizontal = 16.dp, vertical = 8.dp),
            horizontalArrangement = Arrangement.spacedBy(8.dp)
        ) {
            items(categories) { category ->
                Box(
                    modifier = Modifier
                        .clip(RoundedCornerShape(percent = 50))
                        .background(if (selectedCategory == category) Color(0xFFE50914) else Color(0xFF1E1E20))
                        .clickable { selectedCategory = category }
                        .padding(horizontal = 16.dp, vertical = 8.dp),
                    contentAlignment = Alignment.Center
                ) {
                    Row(verticalAlignment = Alignment.CenterVertically) {
                        Text(
                            text = category,
                            color = if (selectedCategory == category) Color.White else Color.LightGray,
                            fontSize = 14.sp,
                            fontWeight = if (selectedCategory == category) FontWeight.SemiBold else FontWeight.Normal
                        )
                        if (category == "Genres") {
                            Spacer(modifier = Modifier.width(4.dp))
                            Icon(Icons.Default.ArrowDropDown, contentDescription = null, tint = Color.LightGray, modifier = Modifier.size(16.dp))
                        }
                    }
                }
            }
        }


        Spacer(modifier = Modifier.height(24.dp))
        
        SectionTitleShared("Continue Watching", onSeeAllClick = onNavigateToWatching)
        ContinueWatchingCardShared()

        Spacer(modifier = Modifier.height(24.dp))

        // Popular Series
        SectionTitleShared("Popular Series", onSeeAllClick = onNavigateToPopular)
        LazyRow(
            contentPadding = PaddingValues(horizontal = 16.dp),
            horizontalArrangement = Arrangement.spacedBy(16.dp)
        ) {
            itemsIndexed(uiState.series) { index, series ->
                MediaCard(
                    title = series.title,
                    posterUrl = series.posterUrl,
                    rank = index + 1,
                    rating = 8.7 - (index * 0.1),
                    year = "${series.seasons.size} Seasons",
                    isMovie = false,
                    onClick = { onSeriesClick(series.id) },
                    onLongClick = { 
                        selectedMediaId = series.id
                        selectedMediaTitle = series.title
                        selectedMediaPoster = series.posterUrl
                        showBottomSheet = true
                    }
                )
            }
        }

        Spacer(modifier = Modifier.height(24.dp))

        // New Releases
        SectionTitleShared("New Releases", onSeeAllClick = onNavigateToNewReleases)
        LazyRow(
            contentPadding = PaddingValues(horizontal = 16.dp),
            horizontalArrangement = Arrangement.spacedBy(16.dp)
        ) {
            itemsIndexed(uiState.series.reversed()) { index, series ->
                MediaCard(
                    title = series.title,
                    posterUrl = series.posterUrl,
                    rank = null, 
                    rating = 8.5,
                    year = "2024",
                    isMovie = false,
                    onClick = { onSeriesClick(series.id) },
                    onLongClick = { 
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
                isMovie = false,
                onDismissRequest = { showBottomSheet = false },
                onDownloadStart = { quality ->
                    scope.launch {
                        downloadRepository.addToDownloads(DownloadItem(
                            id = selectedMediaId,
                            title = selectedMediaTitle,
                            posterUrl = selectedMediaPoster,
                            isMovie = false,
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
                            isMovie = false
                        ))
                        Toast.makeText(context, "Added to Library", Toast.LENGTH_SHORT).show()
                    }
                }
            )
        }
    }
}
