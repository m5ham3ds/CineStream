package com.example.ui.screens.movies

import androidx.compose.foundation.layout.*
import androidx.compose.foundation.lazy.grid.GridCells
import androidx.compose.foundation.lazy.grid.LazyVerticalGrid
import androidx.compose.foundation.lazy.grid.items
import androidx.compose.material3.CircularProgressIndicator
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.collectAsState
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.setValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.unit.dp
import androidx.lifecycle.viewmodel.compose.viewModel
import android.widget.Toast
import androidx.compose.ui.platform.LocalContext
import com.example.ui.ViewModelFactory
import com.example.ui.components.MediaCard
import com.example.ui.components.MediaActionBottomSheet

@Composable
fun MoviesScreen(
    onMovieClick: (String) -> Unit,
    viewModel: MoviesViewModel = viewModel(factory = ViewModelFactory())
) {
    val uiState by viewModel.uiState.collectAsState()
    val context = LocalContext.current
    var showBottomSheet by remember { mutableStateOf(false) }

    Column(modifier = Modifier.fillMaxSize()) {
        Spacer(modifier = Modifier.height(32.dp))
        if (uiState.isLoading) {
            Box(modifier = Modifier.fillMaxSize(), contentAlignment = Alignment.Center) {
                CircularProgressIndicator()
            }
        } else if (uiState.error != null) {
            Box(modifier = Modifier.fillMaxSize(), contentAlignment = Alignment.Center) {
                Text(uiState.error ?: "Error loading movies")
            }
        } else {
            LazyVerticalGrid(
                columns = GridCells.Adaptive(minSize = 120.dp),
                contentPadding = PaddingValues(start = 16.dp, end = 16.dp, bottom = 80.dp),
                horizontalArrangement = Arrangement.spacedBy(16.dp),
                verticalArrangement = Arrangement.spacedBy(16.dp),
                modifier = Modifier.fillMaxSize()
            ) {
                items(uiState.movies) { movie ->
                    MediaCard(
                        title = movie.title,
                        posterUrl = movie.posterUrl,
                        onClick = { onMovieClick(movie.id) },
                        onLongClick = { showBottomSheet = true },
                        modifier = Modifier.fillMaxWidth()
                    )
                }
            }
        }
    }
    
    if (showBottomSheet) {
        MediaActionBottomSheet(
            isMovie = true,
            onDismissRequest = { showBottomSheet = false },
            onDownloadStart = { Toast.makeText(context, "Download Started", Toast.LENGTH_SHORT).show() },
            onAddToLibrary = { Toast.makeText(context, "Added to Library", Toast.LENGTH_SHORT).show() }
        )
    }
}

