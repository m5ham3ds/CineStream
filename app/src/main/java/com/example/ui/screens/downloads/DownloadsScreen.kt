package com.example.ui.screens.downloads

import androidx.compose.foundation.background
import androidx.compose.foundation.border
import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.shape.CircleShape
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.foundation.verticalScroll
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.MoreVert
import androidx.compose.material.icons.filled.PlayArrow
import androidx.compose.material.icons.outlined.CheckCircle
import androidx.compose.material.icons.outlined.Download
import androidx.compose.material.icons.outlined.Edit
import androidx.compose.material.icons.outlined.Folder
import androidx.compose.material.icons.outlined.SdStorage
import androidx.compose.material.icons.outlined.Storage
import androidx.compose.material.icons.outlined.Timer
import androidx.compose.material.icons.outlined.Tv
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.layout.ContentScale
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import androidx.compose.ui.text.style.TextOverflow
import coil.compose.AsyncImage
import com.example.ui.components.SectionTitleShared

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun DownloadsScreen(onItemClick: (String, Boolean) -> Unit = { _, _ -> }) {
    var selectedTab by remember { mutableStateOf("All") }
    val scrollState = rememberScrollState()

    Column(
        modifier = Modifier
            .fillMaxSize()
            .verticalScroll(scrollState)
            .padding(16.dp)
    ) {
        // Header
        Row(
            modifier = Modifier.fillMaxWidth().padding(top = 16.dp),
            horizontalArrangement = Arrangement.SpaceBetween,
            verticalAlignment = Alignment.CenterVertically
        ) {
            Row(verticalAlignment = Alignment.CenterVertically) {
                Icon(Icons.Outlined.Download, contentDescription = null, tint = Color(0xFFE50914), modifier = Modifier.size(28.dp))
                Spacer(modifier = Modifier.width(12.dp))
                Text("Downloads", color = Color.White, fontSize = 28.sp, fontWeight = FontWeight.Bold)
            }
            Row(
                modifier = Modifier
                    .clip(RoundedCornerShape(percent = 50))
                    .border(1.dp, Color.DarkGray, RoundedCornerShape(percent = 50))
                    .clickable { }
                    .padding(horizontal = 12.dp, vertical = 6.dp),
                verticalAlignment = Alignment.CenterVertically
            ) {
                Icon(Icons.Outlined.Edit, contentDescription = null, tint = Color.White, modifier = Modifier.size(16.dp))
                Spacer(modifier = Modifier.width(6.dp))
                Text("Edit", color = Color.White, fontSize = 14.sp)
            }
        }
        
        Spacer(modifier = Modifier.height(8.dp))
        Text("Watch your content offline anytime, anywhere.", color = Color.LightGray, fontSize = 14.sp)
        
        Spacer(modifier = Modifier.height(24.dp))

        // Stats Row
        Row(
            modifier = Modifier
                .fillMaxWidth()
                .clip(RoundedCornerShape(16.dp))
                .background(Color(0xFF161618))
                .border(1.dp, Color(0xFF2A2A2E), RoundedCornerShape(16.dp))
                .padding(vertical = 16.dp),
            horizontalArrangement = Arrangement.SpaceEvenly,
            verticalAlignment = Alignment.CenterVertically
        ) {
            DownloadStat(icon = Icons.Outlined.Folder, value = "1", label = "Downloaded", isPrimary = true)
            Box(modifier = Modifier.width(1.dp).height(32.dp).background(Color(0xFF2A2A2E)))
            DownloadStat(icon = Icons.Outlined.Timer, value = "0", label = "In Progress")
            Box(modifier = Modifier.width(1.dp).height(32.dp).background(Color(0xFF2A2A2E)))
            DownloadStat(icon = Icons.Outlined.CheckCircle, value = "1", label = "Completed")
            Box(modifier = Modifier.width(1.dp).height(32.dp).background(Color(0xFF2A2A2E)))
            DownloadStat(icon = Icons.Outlined.SdStorage, value = "2.4 GB", label = "Used Space")
        }

        Spacer(modifier = Modifier.height(24.dp))

        // Tabs
        Row(horizontalArrangement = Arrangement.spacedBy(8.dp)) {
            listOf("All", "Movies", "Series", "Episodes").forEach { tab ->
                val isSelected = selectedTab == tab
                Box(
                    modifier = Modifier
                        .clip(RoundedCornerShape(percent = 50))
                        .background(if (isSelected) Color(0xFFE50914) else Color(0xFF2A2A2E))
                        .clickable { selectedTab = tab }
                        .padding(horizontal = 16.dp, vertical = 8.dp)
                ) {
                    Text(tab, color = if (isSelected) Color.White else Color.LightGray, fontSize = 14.sp, fontWeight = if (isSelected) FontWeight.Bold else FontWeight.Normal)
                }
            }
        }

        Spacer(modifier = Modifier.height(24.dp))

        // Download Item Card
        Box(
            modifier = Modifier
                .fillMaxWidth()
                .clip(RoundedCornerShape(16.dp))
                .background(Color(0xFF161618))
                .border(1.dp, Color(0xFF2A2A2E), RoundedCornerShape(16.dp))
                .padding(16.dp)
        ) {
            Row {
                AsyncImage(
                    model = "https://images.unsplash.com/photo-1536440136628-849c177e76a1?q=80&w=200&auto=format&fit=crop",
                    contentDescription = null,
                    modifier = Modifier.size(100.dp, 150.dp).clip(RoundedCornerShape(12.dp)),
                    contentScale = ContentScale.Crop
                )
                Spacer(modifier = Modifier.width(16.dp))
                Column(modifier = Modifier.weight(1f)) {
                    Row(modifier = Modifier.fillMaxWidth(), horizontalArrangement = Arrangement.SpaceBetween) {
                        Text("Demo Series 10", color = Color.White, fontSize = 18.sp, fontWeight = FontWeight.Bold, modifier = Modifier.weight(1f))
                        Icon(Icons.Default.MoreVert, contentDescription = "More", tint = Color.LightGray, modifier = Modifier.size(20.dp))
                    }
                    Spacer(modifier = Modifier.height(4.dp))
                    Row(verticalAlignment = Alignment.CenterVertically) {
                        Icon(Icons.Outlined.Tv, contentDescription = null, tint = Color.Gray, modifier = Modifier.size(14.dp))
                        Spacer(modifier = Modifier.width(4.dp))
                        Text("Series • 0 Episodes", color = Color.Gray, fontSize = 12.sp)
                    }
                    Spacer(modifier = Modifier.height(12.dp))
                    Text("1080p (FHD) • 2.4 GB", color = Color.LightGray, fontSize = 14.sp)
                    Spacer(modifier = Modifier.height(12.dp))
                    Row(verticalAlignment = Alignment.CenterVertically) {
                        Icon(Icons.Outlined.CheckCircle, contentDescription = null, tint = Color(0xFF4CAF50), modifier = Modifier.size(16.dp))
                        Spacer(modifier = Modifier.width(4.dp))
                        Text("Downloaded", color = Color(0xFF4CAF50), fontSize = 14.sp, fontWeight = FontWeight.Medium)
                    }
                    Spacer(modifier = Modifier.height(4.dp))
                    Text("May 25, 2024 • 3:42 PM", color = Color.Gray, fontSize = 12.sp)
                }
                
                Box(
                    modifier = Modifier
                        .align(Alignment.Bottom)
                        .padding(start = 8.dp)
                        .size(40.dp)
                        .clip(CircleShape)
                        .background(Color(0xFF2A2A2E)),
                    contentAlignment = Alignment.Center
                ) {
                    Icon(Icons.Default.PlayArrow, contentDescription = "Play", tint = Color.White)
                }
            }
        }

        Spacer(modifier = Modifier.height(16.dp))

        // Storage Card
        Box(
            modifier = Modifier
                .fillMaxWidth()
                .clip(RoundedCornerShape(16.dp))
                .background(Color(0xFF161618))
                .border(1.dp, Color(0xFF2A2A2E), RoundedCornerShape(16.dp))
                .padding(20.dp)
        ) {
            Column {
                Row(modifier = Modifier.fillMaxWidth(), horizontalArrangement = Arrangement.SpaceBetween, verticalAlignment = Alignment.CenterVertically) {
                    Row(verticalAlignment = Alignment.CenterVertically) {
                        Icon(Icons.Outlined.Storage, contentDescription = null, tint = Color(0xFFE50914), modifier = Modifier.size(20.dp))
                        Spacer(modifier = Modifier.width(8.dp))
                        Text("Storage", color = Color.White, fontSize = 16.sp, fontWeight = FontWeight.Bold)
                    }
                    Text("2.4 GB / 50 GB used", color = Color.LightGray, fontSize = 14.sp)
                }
                Spacer(modifier = Modifier.height(16.dp))
                
                // Progress Bar
                Box(modifier = Modifier.fillMaxWidth().height(6.dp).clip(RoundedCornerShape(percent = 50)).background(Color(0xFF2A2A2E))) {
                    Box(modifier = Modifier.fillMaxWidth(0.04f).height(6.dp).clip(RoundedCornerShape(percent = 50)).background(Color(0xFFE50914)))
                }
                
                Spacer(modifier = Modifier.height(12.dp))
                Row(modifier = Modifier.fillMaxWidth(), horizontalArrangement = Arrangement.SpaceBetween) {
                    Text("4% used", color = Color.Gray, fontSize = 12.sp)
                    Text("47.6 GB free", color = Color.Gray, fontSize = 12.sp)
                }
            }
        }

        Spacer(modifier = Modifier.height(16.dp))

        // Download More Card
        Box(
            modifier = Modifier
                .fillMaxWidth()
                .clip(RoundedCornerShape(16.dp))
                .background(Color(0xFF161618))
                .border(1.dp, Color(0xFF2A2A2E), RoundedCornerShape(16.dp))
                .padding(20.dp)
        ) {
            Row(verticalAlignment = Alignment.CenterVertically) {
                Box(modifier = Modifier.size(80.dp), contentAlignment = Alignment.Center) {
                    AsyncImage(
                        model = "https://images.unsplash.com/photo-1485846234645-a62644f84728?q=80&w=200&auto=format&fit=crop",
                        contentDescription = null,
                        modifier = Modifier.size(80.dp).clip(CircleShape),
                        contentScale = ContentScale.Crop,
                        alpha = 0.5f
                    )
                    Box(modifier = Modifier.size(32.dp).clip(RoundedCornerShape(8.dp)).background(Color(0xFF2A2A2E)), contentAlignment = Alignment.Center) {
                        Icon(Icons.Outlined.Download, contentDescription = null, tint = Color(0xFFE50914), modifier = Modifier.size(20.dp))
                    }
                }
                Spacer(modifier = Modifier.width(16.dp))
                Column(modifier = Modifier.weight(1f)) {
                    Text("Download more content", color = Color.White, fontSize = 16.sp, fontWeight = FontWeight.Bold)
                    Spacer(modifier = Modifier.height(4.dp))
                    Text("Find movies and series to download and watch offline.", color = Color.Gray, fontSize = 12.sp, lineHeight = 16.sp)
                    Spacer(modifier = Modifier.height(12.dp))
                    Button(
                        onClick = { },
                        colors = ButtonDefaults.buttonColors(containerColor = Color(0xFF4A1010)), // Dark red
                        shape = RoundedCornerShape(percent = 50),
                        contentPadding = PaddingValues(horizontal = 16.dp, vertical = 0.dp),
                        modifier = Modifier.height(36.dp)
                    ) {
                        Text("Browse Content", color = Color.White, fontSize = 12.sp, fontWeight = FontWeight.SemiBold)
                    }
                }
            }
        }
        
        Spacer(modifier = Modifier.height(100.dp))
    }
}

@Composable
fun DownloadStat(icon: androidx.compose.ui.graphics.vector.ImageVector, value: String, label: String, isPrimary: Boolean = false) {
    Row(verticalAlignment = Alignment.CenterVertically, modifier = Modifier.padding(horizontal = 4.dp)) {
        Box(
            modifier = Modifier
                .size(36.dp)
                .clip(RoundedCornerShape(8.dp))
                .background(if (isPrimary) Color(0xFFE50914).copy(alpha = 0.1f) else Color.Transparent)
                .border(1.dp, if (isPrimary) Color(0xFFE50914) else Color.DarkGray, RoundedCornerShape(8.dp)),
            contentAlignment = Alignment.Center
        ) {
            Icon(icon, contentDescription = null, tint = if (isPrimary) Color(0xFFE50914) else Color.Gray, modifier = Modifier.size(18.dp))
        }
        Spacer(modifier = Modifier.width(6.dp))
        Column {
            Text(value, color = Color.White, fontSize = 16.sp, fontWeight = FontWeight.Bold, maxLines = 1)
            Text(label, color = Color.Gray, fontSize = 10.sp, maxLines = 1, overflow = TextOverflow.Ellipsis)
        }
    }
}
