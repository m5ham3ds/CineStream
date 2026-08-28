package com.example.ui.screens.anime

import androidx.compose.foundation.layout.*
import androidx.compose.foundation.lazy.grid.GridCells
import androidx.compose.foundation.lazy.grid.LazyVerticalGrid
import androidx.compose.foundation.lazy.grid.items
import androidx.compose.material3.CircularProgressIndicator
import androidx.compose.material3.Text
import androidx.compose.material3.ExperimentalMaterial3Api
import androidx.compose.material3.pulltorefresh.PullToRefreshBox
import androidx.compose.material3.pulltorefresh.rememberPullToRefreshState
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.unit.dp
import androidx.lifecycle.viewmodel.compose.viewModel
import com.example.ui.ViewModelFactory
import com.example.ui.components.MediaCard

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun AnimeScreen(
    onAnimeClick: (String) -> Unit,
    viewModel: AnimeViewModel = viewModel(factory = ViewModelFactory())
) {
    val uiState by viewModel.uiState.collectAsState()

    val ptrState = rememberPullToRefreshState()
    PullToRefreshBox(
        isRefreshing = uiState.isLoading,
        onRefresh = { viewModel.loadData() },
        state = ptrState,
        modifier = Modifier.fillMaxSize()
    ) {
        if (uiState.isLoading && uiState.series.isEmpty()) {
            Box(modifier = Modifier.fillMaxSize(), contentAlignment = Alignment.Center) {
                CircularProgressIndicator(color = Color(0xFFE50914))
            }
        } else if (uiState.error != null) {
            Box(modifier = Modifier.fillMaxSize(), contentAlignment = Alignment.Center) {
                Text(uiState.error ?: "Error", color = Color.White)
            }
        } else {
            LazyVerticalGrid(
                columns = GridCells.Fixed(3),
                contentPadding = PaddingValues(16.dp),
                horizontalArrangement = Arrangement.spacedBy(16.dp),
                verticalArrangement = Arrangement.spacedBy(16.dp),
                modifier = Modifier.fillMaxSize()
            ) {
                items(uiState.series) { series ->
                    MediaCard(
                        title = series.title,
                        posterUrl = series.posterUrl,
                        rank = 0,
                        rating = series.rating,
                        year = series.year.toString(),
                        isMovie = false,
                        onClick = { onAnimeClick(series.id) }
                    )
                }
            }
        }
    }
}
