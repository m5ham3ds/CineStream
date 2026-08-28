package com.example.ui.screens.home

import androidx.compose.foundation.background
import androidx.compose.foundation.border
import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.lazy.grid.GridCells
import androidx.compose.foundation.lazy.grid.LazyVerticalGrid
import androidx.compose.foundation.lazy.grid.itemsIndexed
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.automirrored.filled.ArrowBack
import androidx.compose.material.icons.filled.FilterAlt
import androidx.compose.material3.*

import androidx.compose.material3.pulltorefresh.PullToRefreshBox
import androidx.compose.material3.pulltorefresh.rememberPullToRefreshState

import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.text.SpanStyle
import androidx.compose.ui.text.buildAnnotatedString
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.withStyle
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import androidx.lifecycle.viewmodel.compose.viewModel
import com.example.ui.ViewModelFactory
import com.example.ui.components.MediaCard

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun NewReleasesScreen(
    onItemClick: (String, Boolean) -> Unit,
    onBack: () -> Unit,
    viewModel: HomeViewModel = viewModel(factory = ViewModelFactory())
) {
    val uiState by viewModel.uiState.collectAsState()
    var selectedTab by remember { mutableStateOf("All") }

    Column(modifier = Modifier.fillMaxSize().background(Color.Black)) {
        CenterAlignedTopAppBar(
            title = {
                Column(horizontalAlignment = Alignment.CenterHorizontally) {
                    Text(
                        text = buildAnnotatedString {
                            withStyle(style = SpanStyle(color = Color.White)) {
                                append("New ")
                            }
                            withStyle(style = SpanStyle(color = Color(0xFFE50914))) {
                                append("Releases")
                            }
                        },
                        fontWeight = FontWeight.Bold,
                        fontSize = 20.sp
                    )
                    Text("Latest additions", color = Color.Gray, fontSize = 12.sp)
                }
            },
            navigationIcon = {
                IconButton(onClick = onBack) {
                    Box(modifier = Modifier.size(40.dp).clip(RoundedCornerShape(percent = 50)).background(Color(0xFF161618)), contentAlignment = Alignment.Center) {
                        Icon(Icons.AutoMirrored.Filled.ArrowBack, contentDescription = "Back", tint = Color.White, modifier = Modifier.size(20.dp))
                    }
                }
            },
            actions = {
                IconButton(onClick = { }) {
                    Box(modifier = Modifier.size(40.dp).clip(RoundedCornerShape(percent = 50)).background(Color(0xFF161618)), contentAlignment = Alignment.Center) {
                        Icon(Icons.Default.FilterAlt, contentDescription = "Filter", tint = Color.White, modifier = Modifier.size(20.dp))
                    }
                }
            },
            colors = TopAppBarDefaults.centerAlignedTopAppBarColors(containerColor = Color.Black)
        )
        Spacer(modifier = Modifier.height(16.dp))
        
        // Tabs
        Row(
            modifier = Modifier
                .fillMaxWidth()
                .padding(horizontal = 24.dp)
                .height(40.dp)
                .clip(RoundedCornerShape(8.dp))
                .border(1.dp, Color(0xFF2A2A2E), RoundedCornerShape(8.dp)),
        ) {
            listOf("All", "Movies", "Series", "Anime").forEach { tab ->
                val isSelected = selectedTab == tab
                Box(
                    modifier = Modifier
                        .weight(1f)
                        .fillMaxHeight()
                        .background(if (isSelected) Color(0xFF2A2A2E).copy(alpha = 0.3f) else Color.Transparent)
                        .border(
                            width = 1.dp,
                            color = if (isSelected) Color(0xFFE50914) else Color.Transparent,
                            shape = RoundedCornerShape(8.dp)
                        )
                        .clickable { selectedTab = tab },
                    contentAlignment = Alignment.Center
                ) {
                    Text(
                        text = tab,
                        color = if (isSelected) Color.White else Color.Gray,
                        fontWeight = if (isSelected) FontWeight.Bold else FontWeight.Normal,
                        fontSize = 12.sp
                    )
                }
            }
        }
        
        Spacer(modifier = Modifier.height(16.dp))

        val items = when (selectedTab) {
            "Movies" -> uiState.newReleasesMovies
            "Series" -> uiState.newReleasesSeries
            "Anime" -> uiState.animeSeries
            else -> (uiState.newReleasesMovies + uiState.newReleasesSeries + uiState.animeSeries).shuffled()
        }
        val ptrState = rememberPullToRefreshState()
        PullToRefreshBox(
            isRefreshing = uiState.isLoading,
            onRefresh = { viewModel.loadData() },
            state = ptrState,
            modifier = Modifier.fillMaxSize()
        ) {


        LazyVerticalGrid(
            columns = GridCells.Fixed(3),
            contentPadding = PaddingValues(16.dp),
            horizontalArrangement = Arrangement.spacedBy(8.dp),
            verticalArrangement = Arrangement.spacedBy(16.dp),
            modifier = Modifier.fillMaxSize()
        ) {
            itemsIndexed(items) { index, item ->
                val isMovie = item is com.example.domain.models.Movie
                val title = if (isMovie) (item as com.example.domain.models.Movie).title else (item as com.example.domain.models.Series).title
                val posterUrl = if (isMovie) (item as com.example.domain.models.Movie).posterUrl else (item as com.example.domain.models.Series).posterUrl
                val id = if (isMovie) (item as com.example.domain.models.Movie).id else (item as com.example.domain.models.Series).id

                MediaCard(
                    title = title,
                    posterUrl = posterUrl,
                    rank = null, // No rank for new releases
                    rating = 8.0 + (index * 0.1),
                    year = "2024",
                    isMovie = isMovie,
                    mediaId = id,
                    onClick = { onItemClick(id, isMovie) }
                )
            }
        }
    }
}
}
