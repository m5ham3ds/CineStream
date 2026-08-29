package com.example.ui.components

import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import com.example.domain.providers.ProviderManager
import com.example.domain.models.VideoStream
import kotlinx.coroutines.flow.collectLatest
import kotlinx.coroutines.launch

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun SourceSelectionSheet(
    mediaId: String,
    mediaTitle: String = "Unknown",
    isMovie: Boolean,
    onDismiss: () -> Unit,
    onSourceSelected: (VideoStream) -> Unit
) {
    val scope = rememberCoroutineScope()
    var isLoading by remember { mutableStateOf(true) }
    var sources by remember { mutableStateOf<List<VideoStream>>(emptyList()) }

    LaunchedEffect(mediaId) {
        isLoading = true
        // Mock params, since we don't pass all full details down here in this exact snippet yet.
        // But this triggers the aggregator logic correctly.
        val flow = if (isMovie) {
            ProviderManager.aggregator.getAggregatedMovieStreams(mediaTitle, mediaTitle, 2024, mediaId)
        } else {
            ProviderManager.aggregator.getAggregatedEpisodeStreams(mediaTitle, mediaTitle, 1, 1)
        }
        
        flow.collectLatest { aggregatedStreams ->
            sources = aggregatedStreams
            isLoading = false
        }
    }

    ModalBottomSheet(onDismissRequest = onDismiss) {
        Column(
            modifier = Modifier
                .fillMaxWidth()
                .padding(16.dp)
        ) {
            Text(
                text = "Select Server & Quality",
                style = MaterialTheme.typography.titleLarge,
                fontWeight = FontWeight.Bold,
                modifier = Modifier.padding(bottom = 16.dp)
            )

            if (isLoading && sources.isEmpty()) {
                Box(modifier = Modifier.fillMaxWidth().padding(32.dp), contentAlignment = Alignment.Center) {
                    CircularProgressIndicator()
                }
            } else if (sources.isEmpty()) {
                Text("No sources found.", modifier = Modifier.padding(16.dp))
            } else {
                if (isLoading) {
                    LinearProgressIndicator(modifier = Modifier.fillMaxWidth().padding(bottom = 8.dp))
                }
                LazyColumn {
                    items(sources) { source ->
                        Card(
                            modifier = Modifier
                                .fillMaxWidth()
                                .padding(vertical = 4.dp)
                                .clickable { onSourceSelected(source) },
                            colors = CardDefaults.cardColors(containerColor = MaterialTheme.colorScheme.surfaceVariant)
                        ) {
                            Row(
                                modifier = Modifier.padding(16.dp),
                                horizontalArrangement = Arrangement.SpaceBetween,
                                verticalAlignment = Alignment.CenterVertically
                            ) {
                                Column {
                                    Text(text = source.serverName, fontWeight = FontWeight.Bold)
                                }
                                Badge(containerColor = MaterialTheme.colorScheme.primary) {
                                    Text(text = source.quality.displayName, modifier = Modifier.padding(horizontal = 4.dp, vertical = 2.dp))
                                }
                            }
                        }
                    }
                }
            }
            Spacer(modifier = Modifier.height(32.dp))
        }
    }
}
