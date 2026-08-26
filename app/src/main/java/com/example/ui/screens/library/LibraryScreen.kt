package com.example.ui.screens.library

import androidx.compose.foundation.layout.*
import androidx.compose.foundation.lazy.grid.GridCells
import androidx.compose.foundation.lazy.grid.LazyVerticalGrid
import androidx.compose.foundation.lazy.grid.items
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Text
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import com.example.data.repository.LibraryRepository
import com.example.ui.components.MediaCard
import kotlinx.coroutines.launch

@Composable
fun LibraryScreen(onItemClick: (String, Boolean) -> Unit = { _, _ -> }) {
    val context = LocalContext.current
    val libraryRepository = remember { LibraryRepository(context) }
    val items by libraryRepository.getLibraryItems().collectAsState(initial = emptyList())

    Column(
        modifier = Modifier
            .fillMaxSize()
            .padding(16.dp),
        horizontalAlignment = Alignment.CenterHorizontally
    ) {
        Text(
            text = "My Library",
            style = MaterialTheme.typography.headlineMedium,
            fontWeight = FontWeight.Bold,
            color = androidx.compose.ui.graphics.Color.White,
            modifier = Modifier.padding(bottom = 24.dp)
        )

        if (items.isEmpty()) {
            Spacer(modifier = Modifier.weight(1f))
            Text(
                text = "Your Watchlist and History will appear here.",
                style = MaterialTheme.typography.bodyLarge,
                color = MaterialTheme.colorScheme.onSurfaceVariant
            )
            Spacer(modifier = Modifier.weight(1f))
        } else {
            LazyVerticalGrid(
                columns = GridCells.Fixed(2),
                horizontalArrangement = Arrangement.spacedBy(16.dp),
                verticalArrangement = Arrangement.spacedBy(16.dp),
                contentPadding = PaddingValues(bottom = 80.dp)
            ) {
                items(items) { item ->
                    MediaCard(
                        title = item.title,
                        posterUrl = item.posterUrl,
                        onClick = { onItemClick(item.id, item.isMovie) },
                        onLongClick = { /* Maybe remove? */ }
                    )
                }
            }
        }
    }
}
