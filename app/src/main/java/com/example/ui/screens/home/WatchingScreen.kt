package com.example.ui.screens.home

import androidx.compose.foundation.background
import androidx.compose.foundation.border
import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.shape.CircleShape
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.automirrored.filled.ArrowBack
import androidx.compose.material.icons.filled.MoreVert
import androidx.compose.material.icons.filled.PlayArrow
import androidx.compose.material3.*
import androidx.compose.runtime.Composable
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.layout.ContentScale
import androidx.compose.ui.text.SpanStyle
import androidx.compose.ui.text.buildAnnotatedString
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.withStyle
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import coil.compose.AsyncImage

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun WatchingScreen(
    onItemClick: (String, Boolean) -> Unit,
    onBack: () -> Unit
) {
    Column(modifier = Modifier.fillMaxSize().background(Color.Black)) {
        CenterAlignedTopAppBar(
            title = {
                Column(horizontalAlignment = Alignment.CenterHorizontally) {
                    Text("Continue Watching", color = Color.White, fontWeight = FontWeight.Bold, fontSize = 20.sp)
                }
            },
            navigationIcon = {
                IconButton(onClick = onBack) {
                    Icon(Icons.AutoMirrored.Filled.ArrowBack, contentDescription = "Back", tint = Color.White)
                }
            },
            colors = TopAppBarDefaults.centerAlignedTopAppBarColors(containerColor = Color.Black)
        )
        
        Text(
            text = "Pick up where you left off",
            color = Color.Gray,
            fontSize = 14.sp,
            modifier = Modifier.padding(start = 24.dp, bottom = 16.dp)
        )

        LazyColumn(
            contentPadding = PaddingValues(start = 16.dp, end = 16.dp, top = 8.dp, bottom = 100.dp),
            verticalArrangement = Arrangement.spacedBy(16.dp),
            modifier = Modifier.fillMaxSize()
        ) {
            val items = listOf(
                DetailedWatchingItem("Demo Series 01", "TV Series", "S1 • E3", "24m left", "of 48m", 0.5f, "https://image.tmdb.org/t/p/w500/8Y43POKjjKDGI9MH89NW0NAzzp8.jpg"),
                DetailedWatchingItem("Demo Series 02", "TV Series", "S2 • E5", "18m left", "of 45m", 0.6f, "https://image.tmdb.org/t/p/w500/zSpKGOSQAE3O52eGqE1Hj5K7qU3.jpg"),
                DetailedWatchingItem("Demo Movie 03", "Movie", "", "1h 12m left", "of 2h 4m", 0.4f, "https://image.tmdb.org/t/p/w500/yDHYTfA3R0jFYba16ZBRWJCBpz2.jpg"),
                DetailedWatchingItem("Demo Movie 04", "Movie", "", "36m left", "of 1h 58m", 0.7f, "https://images.unsplash.com/photo-1485846234645-a62644f84728?q=80&w=2000&auto=format&fit=crop")
            )
            
            items(items.size) { index ->
                DetailedContinueWatchingCard(items[index])
            }
        }
    }
}

data class DetailedWatchingItem(
    val title: String,
    val type: String,
    val episodeInfo: String,
    val timeLeft: String,
    val totalTime: String,
    val progress: Float,
    val imageUrl: String
)

@Composable
fun DetailedContinueWatchingCard(item: DetailedWatchingItem) {
    Box(
        modifier = Modifier
            .fillMaxWidth()
            .clip(RoundedCornerShape(12.dp))
            .background(Color(0xFF161618))
            .clickable { /* Resume */ }
    ) {
        Row(
            modifier = Modifier.fillMaxWidth().height(140.dp)
        ) {
            // Image Section
            Box(modifier = Modifier.weight(1.2f).fillMaxHeight()) {
                AsyncImage(
                    model = item.imageUrl,
                    contentDescription = item.title,
                    contentScale = ContentScale.Crop,
                    modifier = Modifier.fillMaxSize()
                )
                
                // Dark overlay
                Box(modifier = Modifier.fillMaxSize().background(Color.Black.copy(alpha = 0.3f)))
                
                // Play Button
                Box(
                    modifier = Modifier
                        .align(Alignment.Center)
                        .size(40.dp)
                        .clip(CircleShape)
                        .background(Color.Black.copy(alpha = 0.6f))
                        .border(1.dp, Color.White.copy(alpha = 0.3f), CircleShape),
                    contentAlignment = Alignment.Center
                ) {
                    Icon(Icons.Default.PlayArrow, contentDescription = "Play", tint = Color.White, modifier = Modifier.size(20.dp))
                }
                
                // Progress Bar at bottom of image
                Box(modifier = Modifier.align(Alignment.BottomStart).fillMaxWidth().height(4.dp).background(Color(0xFF2A2A2E))) {
                    Box(modifier = Modifier.fillMaxWidth(item.progress).height(4.dp).background(Color(0xFFE50914)))
                }
            }
            
            // Details Section
            Column(
                modifier = Modifier
                    .weight(1.5f)
                    .fillMaxHeight()
                    .padding(12.dp)
            ) {
                // Type Badge
                Box(
                    modifier = Modifier
                        .clip(RoundedCornerShape(4.dp))
                        .background(Color(0xFFE50914).copy(alpha = 0.15f))
                        .padding(horizontal = 6.dp, vertical = 2.dp)
                ) {
                    Text(item.type, color = Color(0xFFE50914), fontSize = 10.sp, fontWeight = FontWeight.Medium)
                }
                
                Spacer(modifier = Modifier.height(8.dp))
                
                Text(item.title, color = Color.White, fontWeight = FontWeight.Bold, fontSize = 16.sp)
                
                if (item.episodeInfo.isNotEmpty()) {
                    Spacer(modifier = Modifier.height(2.dp))
                    Text(item.episodeInfo, color = Color.Gray, fontSize = 12.sp)
                }
                
                Spacer(modifier = Modifier.height(12.dp))
                
                Text(
                    text = buildAnnotatedString {
                        withStyle(style = SpanStyle(color = Color(0xFFE50914), fontWeight = FontWeight.Bold)) {
                            append(item.timeLeft)
                        }
                        withStyle(style = SpanStyle(color = Color.Gray)) {
                            append(" ${item.totalTime}")
                        }
                    },
                    fontSize = 12.sp
                )
                
                Spacer(modifier = Modifier.height(6.dp))
                
                // Progress Bar in text section
                Box(modifier = Modifier.fillMaxWidth().height(2.dp).background(Color(0xFF2A2A2E))) {
                    Box(modifier = Modifier.fillMaxWidth(item.progress).height(2.dp).background(Color(0xFFE50914)))
                }
                
                Spacer(modifier = Modifier.weight(1f))
                
                // Bottom actions
                Row(
                    modifier = Modifier.fillMaxWidth(),
                    horizontalArrangement = Arrangement.End,
                    verticalAlignment = Alignment.CenterVertically
                ) {
                    Box(
                        modifier = Modifier
                            .size(32.dp)
                            .clip(CircleShape)
                            .background(Color(0xFF2A2A2E)),
                        contentAlignment = Alignment.Center
                    ) {
                        Icon(Icons.Default.PlayArrow, contentDescription = "Play", tint = Color(0xFFE50914), modifier = Modifier.size(16.dp))
                    }
                    Spacer(modifier = Modifier.width(12.dp))
                    Icon(Icons.Default.MoreVert, contentDescription = "More", tint = Color.Gray, modifier = Modifier.size(20.dp))
                }
            }
        }
    }
}
