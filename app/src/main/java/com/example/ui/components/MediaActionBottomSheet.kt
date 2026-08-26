package com.example.ui.components

import androidx.compose.foundation.background
import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.Download
import androidx.compose.material.icons.filled.Favorite
import androidx.compose.material.icons.filled.PlayArrow
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import kotlinx.coroutines.launch

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun MediaActionBottomSheet(
    isMovie: Boolean,
    onDismissRequest: () -> Unit,
    onDownloadStart: (String) -> Unit,
    onAddToLibrary: () -> Unit
) {
    val sheetState = rememberModalBottomSheetState(skipPartiallyExpanded = true)
    val scope = rememberCoroutineScope()
    
    var step by remember { mutableStateOf(if (isMovie) 2 else 0) } // 0 = episode select, 1 = episode quality, 2 = movie quality

    ModalBottomSheet(
        onDismissRequest = onDismissRequest,
        sheetState = sheetState,
        containerColor = Color(0xFF1E1E20),
        shape = RoundedCornerShape(topStart = 24.dp, topEnd = 24.dp)
    ) {
        Column(
            modifier = Modifier
                .fillMaxWidth()
                .padding(horizontal = 24.dp, vertical = 16.dp)
        ) {
            when (step) {
                0 -> {
                    Text("Select Episode", color = Color.White, style = MaterialTheme.typography.titleLarge, fontWeight = FontWeight.Bold)
                    Spacer(modifier = Modifier.height(16.dp))
                    (1..5).forEach { ep ->
                        Row(
                            modifier = Modifier
                                .fillMaxWidth()
                                .clip(RoundedCornerShape(12.dp))
                                .clickable { step = 1 }
                                .padding(vertical = 14.dp, horizontal = 12.dp),
                            verticalAlignment = Alignment.CenterVertically
                        ) {
                            Icon(Icons.Default.PlayArrow, contentDescription = null, tint = Color.LightGray)
                            Spacer(modifier = Modifier.width(16.dp))
                            Text(text = "Episode $ep", color = Color.White, fontSize = 16.sp)
                        }
                    }
                }
                1, 2 -> {
                    Text("Download Quality", color = Color.White, style = MaterialTheme.typography.titleLarge, fontWeight = FontWeight.Bold)
                    Spacer(modifier = Modifier.height(16.dp))
                    val qualities = listOf("1080p (FHD)", "720p (HD)", "480p (SD)")
                    qualities.forEach { quality ->
                        Row(
                            modifier = Modifier
                                .fillMaxWidth()
                                .clip(RoundedCornerShape(12.dp))
                                .clickable {
                                    scope.launch { sheetState.hide() }.invokeOnCompletion { 
                                        if (!sheetState.isVisible) {
                                            onDownloadStart(quality)
                                        }
                                    }
                                }
                                .padding(vertical = 14.dp, horizontal = 12.dp),
                            verticalAlignment = Alignment.CenterVertically
                        ) {
                            Icon(Icons.Default.Download, contentDescription = null, tint = Color(0xFFA51B1B))
                            Spacer(modifier = Modifier.width(16.dp))
                            Text(text = quality, color = Color.White, fontSize = 16.sp)
                        }
                    }
                }
            }
            
            if (step == 0 || step == 2) {
                Spacer(modifier = Modifier.height(16.dp))
                HorizontalDivider(color = Color.DarkGray)
                Spacer(modifier = Modifier.height(16.dp))
                Row(
                    modifier = Modifier
                        .fillMaxWidth()
                        .clip(RoundedCornerShape(12.dp))
                        .clickable {
                            scope.launch { sheetState.hide() }.invokeOnCompletion { 
                                if (!sheetState.isVisible) {
                                    onAddToLibrary()
                                }
                            }
                        }
                        .padding(vertical = 14.dp, horizontal = 12.dp),
                    verticalAlignment = Alignment.CenterVertically
                ) {
                    Icon(Icons.Default.Favorite, contentDescription = null, tint = Color(0xFFA51B1B))
                    Spacer(modifier = Modifier.width(16.dp))
                    Text(text = "Add to Library / Favorites", color = Color.White, fontSize = 16.sp)
                }
            }
            
            Spacer(modifier = Modifier.height(32.dp))
        }
    }
}
