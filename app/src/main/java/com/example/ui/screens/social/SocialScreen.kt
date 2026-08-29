package com.example.ui.screens.social

import androidx.compose.foundation.background
import androidx.compose.foundation.border
import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.LazyRow
import androidx.compose.foundation.lazy.items
import androidx.compose.foundation.shape.CircleShape
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.automirrored.filled.ArrowBack
import androidx.compose.material.icons.filled.Add
import androidx.compose.material.icons.filled.PersonAdd
import androidx.compose.material.icons.filled.Search
import androidx.compose.material.icons.outlined.Tune
import androidx.compose.material.icons.automirrored.filled.KeyboardArrowRight
import androidx.compose.material.icons.filled.Group
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import com.example.domain.models.Movie
import com.example.domain.models.Series

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun SocialScreen(
    downloads: List<Any> = emptyList(), // Use Any to combine downloaded movies/series in UI
    library: List<Any> = emptyList(),
    onBack: () -> Unit
) {
    var searchQuery by remember { mutableStateOf("") }
    var showAddStoryDialog by remember { mutableStateOf(false) }

    val stories = remember { listOf("Ahmed", "Sara", "Mohamed", "Ali") }
    
    data class MessageItem(val name: String, val text: String, val time: String, val unreadCount: Int, val isGroup: Boolean = false)
    val messages = remember { listOf(
        MessageItem("Ahmed", "Hey! How are you doing?", "12:45 PM", 2),
        MessageItem("Sara", "Let's watch this tonight \uD83D\uDD25", "11:30 AM", 1),
        MessageItem("Ali", "Thanks! I'll check it out.", "Yesterday", 0),
        MessageItem("Movie Buddies \uD83C\uDF7F", "Mohamed: That was insane!", "Yesterday", 0, isGroup = true),
        MessageItem("Mohamed", "See you tomorrow!", "Mon", 0),
        MessageItem("Nour", "Sent a photo", "Sun", 0)
    )}

    Scaffold(
        topBar = {
            TopAppBar(
                title = { Text("Community", fontWeight = FontWeight.Bold) },
                navigationIcon = {
                    IconButton(onClick = onBack) { Icon(Icons.AutoMirrored.Filled.ArrowBack, contentDescription = "Back") }
                },
                colors = TopAppBarDefaults.topAppBarColors(containerColor = MaterialTheme.colorScheme.background)
            )
        },
        containerColor = MaterialTheme.colorScheme.background
    ) { padding ->
        Column(
            modifier = Modifier
                .fillMaxSize()
                .padding(padding)
        ) {
            // Search Users
            OutlinedTextField(
                value = searchQuery,
                onValueChange = { searchQuery = it },
                modifier = Modifier
                    .fillMaxWidth()
                    .padding(horizontal = 16.dp, vertical = 8.dp),
                placeholder = { Text("Search by username to message...", color = MaterialTheme.colorScheme.onSurfaceVariant) },
                leadingIcon = { Icon(Icons.Default.Search, contentDescription = null, tint = MaterialTheme.colorScheme.onSurfaceVariant) },
                trailingIcon = {
                    Icon(Icons.Outlined.Tune, contentDescription = "Filter", tint = MaterialTheme.colorScheme.onSurfaceVariant)
                },
                shape = RoundedCornerShape(24.dp),
                colors = OutlinedTextFieldDefaults.colors(
                    unfocusedContainerColor = MaterialTheme.colorScheme.surfaceVariant.copy(alpha = 0.2f),
                    focusedContainerColor = MaterialTheme.colorScheme.surfaceVariant.copy(alpha = 0.2f),
                    unfocusedBorderColor = MaterialTheme.colorScheme.primary,
                    focusedBorderColor = MaterialTheme.colorScheme.primary
                )
            )

            // Stories Header
            Row(
                modifier = Modifier.fillMaxWidth().padding(horizontal = 16.dp, vertical = 12.dp),
                horizontalArrangement = Arrangement.SpaceBetween,
                verticalAlignment = Alignment.CenterVertically
            ) {
                Text("Stories", fontWeight = FontWeight.Bold, fontSize = 18.sp, color = MaterialTheme.colorScheme.onBackground)
                Text("View all", color = MaterialTheme.colorScheme.primary, fontSize = 14.sp)
            }

            // Stories Row
            LazyRow(
                contentPadding = PaddingValues(horizontal = 16.dp),
                horizontalArrangement = Arrangement.spacedBy(16.dp)
            ) {
                // Add Story Button
                item {
                    Column(horizontalAlignment = Alignment.CenterHorizontally) {
                        Box(
                            modifier = Modifier
                                .size(72.dp)
                                .clip(CircleShape)
                                .border(2.dp, MaterialTheme.colorScheme.primary, CircleShape)
                                .clickable { showAddStoryDialog = true },
                            contentAlignment = Alignment.Center
                        ) {
                            Icon(Icons.Default.Add, contentDescription = "Add Story", tint = MaterialTheme.colorScheme.primary, modifier = Modifier.size(32.dp))
                        }
                        Spacer(modifier = Modifier.height(8.dp))
                        Text("Add Story", fontSize = 12.sp, color = MaterialTheme.colorScheme.onBackground)
                    }
                }

                items(stories) { user ->
                    Column(horizontalAlignment = Alignment.CenterHorizontally) {
                        Box(
                            modifier = Modifier
                                .size(72.dp)
                                .clip(CircleShape)
                                .background(MaterialTheme.colorScheme.surfaceVariant)
                                .border(2.dp, MaterialTheme.colorScheme.primary, CircleShape),
                            contentAlignment = Alignment.Center
                        ) {
                            // Avatar Placeholder
                            Text(user.take(1), fontSize = 28.sp, color = MaterialTheme.colorScheme.onSurfaceVariant)
                        }
                        Spacer(modifier = Modifier.height(8.dp))
                        Row(verticalAlignment = Alignment.CenterVertically) {
                            Text(user, fontSize = 12.sp, color = MaterialTheme.colorScheme.onBackground)
                            Spacer(modifier = Modifier.width(4.dp))
                            Box(modifier = Modifier.size(8.dp).clip(CircleShape).background(if (user == "Ahmed" || user == "Sara") Color.Green else Color.Gray))
                        }
                    }
                }
            }

            Spacer(modifier = Modifier.height(16.dp))

            // Chips Row
            LazyRow(
                contentPadding = PaddingValues(horizontal = 16.dp),
                horizontalArrangement = Arrangement.spacedBy(8.dp),
                modifier = Modifier.padding(bottom = 16.dp)
            ) {
                item {
                    ChipItem("All Messages", isSelected = true)
                }
                item {
                    ChipItem("Unread", isSelected = false, badge = "2")
                }
                item {
                    ChipItem("Groups", isSelected = false)
                }
                item {
                    ChipItem("Requests", isSelected = false)
                }
            }

            // Messages List
            LazyColumn(
                contentPadding = PaddingValues(bottom = 100.dp, start = 16.dp, end = 16.dp),
                verticalArrangement = Arrangement.spacedBy(8.dp)
            ) {
                items(messages) { msg ->
                    Card(
                        modifier = Modifier.fillMaxWidth().clickable { },
                        shape = RoundedCornerShape(16.dp),
                        colors = CardDefaults.cardColors(containerColor = MaterialTheme.colorScheme.surfaceVariant.copy(alpha = 0.3f))
                    ) {
                        Row(
                            modifier = Modifier.padding(16.dp),
                            verticalAlignment = Alignment.CenterVertically
                        ) {
                            // Avatar
                            Box(contentAlignment = Alignment.BottomEnd) {
                                Box(
                                    modifier = Modifier.size(56.dp).clip(CircleShape).background(MaterialTheme.colorScheme.surfaceVariant),
                                    contentAlignment = Alignment.Center
                                ) {
                                    if (msg.isGroup) {
                                        Icon(Icons.Default.Group, contentDescription = null, tint = MaterialTheme.colorScheme.onSurfaceVariant)
                                    } else {
                                        Text(msg.name.take(1), fontSize = 24.sp, color = MaterialTheme.colorScheme.onSurfaceVariant)
                                    }
                                }
                                Box(
                                    modifier = Modifier.size(14.dp).clip(CircleShape).background(if (msg.unreadCount > 0 || msg.isGroup) Color.Green else Color.Gray).border(2.dp, MaterialTheme.colorScheme.background, CircleShape)
                                )
                            }
                            
                            Spacer(modifier = Modifier.width(16.dp))
                            
                            // Text content
                            Column(modifier = Modifier.weight(1f)) {
                                Text(msg.name, fontWeight = FontWeight.Bold, color = MaterialTheme.colorScheme.onBackground, fontSize = 16.sp)
                                Spacer(modifier = Modifier.height(4.dp))
                                Text(msg.text, fontSize = 14.sp, color = MaterialTheme.colorScheme.onSurfaceVariant, maxLines = 1)
                            }
                            
                            // Time and Badge
                            Column(horizontalAlignment = Alignment.End) {
                                Text(msg.time, fontSize = 12.sp, color = if (msg.unreadCount > 0) MaterialTheme.colorScheme.primary else MaterialTheme.colorScheme.onSurfaceVariant)
                                Spacer(modifier = Modifier.height(8.dp))
                                if (msg.unreadCount > 0) {
                                    Box(
                                        modifier = Modifier.size(24.dp).clip(CircleShape).background(MaterialTheme.colorScheme.primary),
                                        contentAlignment = Alignment.Center
                                    ) {
                                        Text(msg.unreadCount.toString(), color = Color.White, fontSize = 12.sp, fontWeight = FontWeight.Bold)
                                    }
                                } else {
                                    Icon(Icons.AutoMirrored.Filled.KeyboardArrowRight, contentDescription = null, tint = MaterialTheme.colorScheme.onSurfaceVariant, modifier = Modifier.size(20.dp))
                                }
                            }
                        }
                    }
                }
            }
        }
    }

    if (showAddStoryDialog) {
        AlertDialog(
            onDismissRequest = { showAddStoryDialog = false },
            title = { Text("Create Story") },
            text = {
                Column {
                    Text("Select a movie or series you've watched or downloaded to share as a story:", color = MaterialTheme.colorScheme.onSurfaceVariant, fontSize = 14.sp)
                    Spacer(modifier = Modifier.height(16.dp))
                    
                    val availableMedia = (downloads.map { "Download Item" } + library.map { "Library Item" }).distinct()
                    
                    LazyColumn(modifier = Modifier.fillMaxWidth().heightIn(max = 300.dp)) {
                        if (availableMedia.isEmpty()) {
                            item { Text("No media found in library or downloads.", color = MaterialTheme.colorScheme.error) }
                        }
                        items(availableMedia) { title ->
                            Text(
                                text = title,
                                modifier = Modifier
                                    .fillMaxWidth()
                                    .clickable { showAddStoryDialog = false }
                                    .padding(vertical = 12.dp),
                                color = MaterialTheme.colorScheme.onBackground
                            )
                        }
                    }
                }
            },
            confirmButton = {
                TextButton(onClick = { showAddStoryDialog = false }) { Text("Cancel") }
            }
        )
    }
}

@Composable
fun ChipItem(text: String, isSelected: Boolean, badge: String? = null) {
    Surface(
        shape = RoundedCornerShape(20.dp),
        color = if (isSelected) MaterialTheme.colorScheme.primary else MaterialTheme.colorScheme.surfaceVariant.copy(alpha = 0.5f),
        modifier = Modifier.clickable { }
    ) {
        Row(
            modifier = Modifier.padding(horizontal = 16.dp, vertical = 8.dp),
            verticalAlignment = Alignment.CenterVertically
        ) {
            Text(
                text = text,
                color = if (isSelected) Color.White else MaterialTheme.colorScheme.onBackground,
                fontWeight = FontWeight.Bold,
                fontSize = 14.sp
            )
            if (badge != null) {
                Spacer(modifier = Modifier.width(6.dp))
                Box(
                    modifier = Modifier.size(18.dp).clip(CircleShape).background(MaterialTheme.colorScheme.primary),
                    contentAlignment = Alignment.Center
                ) {
                    Text(badge, color = Color.White, fontSize = 10.sp, fontWeight = FontWeight.Bold)
                }
            }
        }
    }
}
