package com.example.ui.components

import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.*
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import kotlinx.coroutines.launch

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun MediaActionBottomSheet(
    isMovie: Boolean,
    onDismissRequest: () -> Unit,
    onDownloadStart: () -> Unit,
    onAddToLibrary: () -> Unit
) {
    val sheetState = rememberModalBottomSheetState(skipPartiallyExpanded = true)
    val scope = rememberCoroutineScope()
    
    var step by remember { mutableStateOf(if (isMovie) 2 else 0) } // 0 = episode select, 1 = episode quality, 2 = movie quality
    
    ModalBottomSheet(
        onDismissRequest = onDismissRequest,
        sheetState = sheetState,
        containerColor = Color(0xFF1E1E20)
    ) {
        Column(
            modifier = Modifier
                .fillMaxWidth()
                .padding(16.dp)
        ) {
            when (step) {
                0 -> {
                    Text("Select Episode", color = Color.White, style = MaterialTheme.typography.titleLarge)
                    Spacer(modifier = Modifier.height(16.dp))
                    (1..5).forEach { ep ->
                        Text(
                            text = "Episode $ep",
                            color = Color.White,
                            modifier = Modifier
                                .fillMaxWidth()
                                .clickable { step = 1 }
                                .padding(vertical = 12.dp)
                        )
                    }
                }
                1, 2 -> {
                    Text("Select Quality", color = Color.White, style = MaterialTheme.typography.titleLarge)
                    Spacer(modifier = Modifier.height(16.dp))
                    val qualities = listOf("1080p (FHD)", "720p (HD)", "480p (SD)")
                    qualities.forEach { quality ->
                        Text(
                            text = quality,
                            color = Color.White,
                            modifier = Modifier
                                .fillMaxWidth()
                                .clickable {
                                    scope.launch { sheetState.hide() }.invokeOnCompletion { 
                                        if (!sheetState.isVisible) {
                                            onDownloadStart()
                                        }
                                    }
                                }
                                .padding(vertical = 12.dp)
                        )
                    }
                }
            }
            
            if (step == 0 || step == 2) {
                Spacer(modifier = Modifier.height(16.dp))
                Divider(color = Color.DarkGray)
                Spacer(modifier = Modifier.height(16.dp))
                Text(
                    text = "Add to Library / Favorites",
                    color = MaterialTheme.colorScheme.primary,
                    modifier = Modifier
                        .fillMaxWidth()
                        .clickable {
                            scope.launch { sheetState.hide() }.invokeOnCompletion { 
                                if (!sheetState.isVisible) {
                                    onAddToLibrary()
                                }
                            }
                        }
                        .padding(vertical = 12.dp)
                )
            }
            
            Spacer(modifier = Modifier.height(32.dp))
        }
    }
}
