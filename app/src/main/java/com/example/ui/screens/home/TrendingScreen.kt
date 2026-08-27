package com.example.ui.screens.home

import androidx.compose.foundation.background
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.lazy.grid.GridCells
import androidx.compose.foundation.lazy.grid.LazyVerticalGrid
import androidx.compose.foundation.lazy.grid.itemsIndexed
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.automirrored.filled.ArrowBack
import androidx.compose.material3.*
import androidx.compose.runtime.Composable
import androidx.compose.runtime.collectAsState
import androidx.compose.runtime.getValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import androidx.lifecycle.viewmodel.compose.viewModel
import com.example.ui.ViewModelFactory
import com.example.ui.components.MediaCard

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun TrendingScreen(
    onItemClick: (String, Boolean) -> Unit,
    onBack: () -> Unit,
    viewModel: HomeViewModel = viewModel(factory = ViewModelFactory())
) {
    val uiState by viewModel.uiState.collectAsState()

    Column(modifier = Modifier.fillMaxSize().background(Color.Black)) {
        CenterAlignedTopAppBar(
            title = { Text("Trending Now", color = Color.White, fontWeight = FontWeight.Bold) },
            navigationIcon = {
                IconButton(onClick = onBack) {
                    Icon(Icons.AutoMirrored.Filled.ArrowBack, contentDescription = "Back", tint = Color.White)
                }
            },
            colors = TopAppBarDefaults.centerAlignedTopAppBarColors(containerColor = Color.Black)
        )

        LazyVerticalGrid(
            columns = GridCells.Fixed(3),
            contentPadding = PaddingValues(16.dp),
            horizontalArrangement = Arrangement.spacedBy(8.dp),
            verticalArrangement = Arrangement.spacedBy(16.dp),
            modifier = Modifier.fillMaxSize()
        ) {
            itemsIndexed(uiState.trendingMovies + uiState.trendingSeries) { index, item ->
                val isMovie = index < uiState.trendingMovies.size
                val title = if (item is com.example.domain.models.Movie) item.title else (item as com.example.domain.models.Series).title
                val posterUrl = if (item is com.example.domain.models.Movie) item.posterUrl else (item as com.example.domain.models.Series).posterUrl
                val id = if (item is com.example.domain.models.Movie) item.id else (item as com.example.domain.models.Series).id
                MediaCard(
                    title = title,
                    posterUrl = posterUrl,
                    rank = index + 1,
                    rating = 8.0 + (index * 0.1),
                    year = "2024",
                    isMovie = isMovie,
                    onClick = { onItemClick(id, isMovie) }
                )
            }
        }
    }
}
