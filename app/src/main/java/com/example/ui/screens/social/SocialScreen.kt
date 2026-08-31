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
import androidx.compose.material.icons.filled.Add
import androidx.compose.material.icons.filled.Search
import androidx.compose.material.icons.filled.Tune
import androidx.compose.material.icons.automirrored.filled.KeyboardArrowRight
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.layout.ContentScale
import androidx.compose.ui.res.painterResource
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import coil.compose.AsyncImage
import com.example.R

data class SocialScreenChatMock(val name: String, val message: String, val time: String, val unread: Int, val isOnline: Boolean, val isGroup: Boolean = false)
data class StoryMock(val name: String, val isOnline: Boolean, val imageUrl: String?)

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun SocialScreen(
    viewModel: SocialViewModel = androidx.lifecycle.viewmodel.compose.viewModel(),
    onBack: () -> Unit = {}
) {
    val currentUser by viewModel.currentUser.collectAsState()
    
    val primaryRed = Color(0xFFE50914)
    val bgColor = Color(0xFF121212)
    val surfaceColor = Color(0xFF1C1C1E)
    
    var searchQuery by remember { mutableStateOf("") }
    
    val stories = listOf(
        StoryMock("Ahmed", true, null),
        StoryMock("Sara", true, null),
        StoryMock("Mohamed", false, null),
        StoryMock("Ali", false, null)
    )
    
    val chats = listOf(
        SocialScreenChatMock("Ahmed", "Hey! How are you doing?", "12:45 PM", 2, true, false),
        SocialScreenChatMock("Sara", "Let's watch this tonight 🔥", "11:30 AM", 1, true, false),
        SocialScreenChatMock("Ali", "Thanks! I'll check it out.", "Yesterday", 0, false, false),
        SocialScreenChatMock("Movie Buddies", "Mohamed: That was insane!", "Yesterday", 0, true, true),
        SocialScreenChatMock("Mohamed", "See you tomorrow!", "Mon", 0, false, false),
        SocialScreenChatMock("Nour", "Sent a photo", "Sun", 0, false, false)
    )

    if (currentUser == null) {
        Box(modifier = Modifier.fillMaxSize().background(bgColor), contentAlignment = Alignment.Center) {
            Column(horizontalAlignment = Alignment.CenterHorizontally) {
                Text("CineStream Community", fontSize = 24.sp, fontWeight = FontWeight.Bold, color = Color.White)
                Spacer(modifier = Modifier.height(8.dp))
                Text("Sign in to chat and share with others", color = Color.Gray)
            }
        }
    } else {
        Column(
            modifier = Modifier
                .fillMaxSize()
                .background(bgColor)
        ) {
            // Header / Search Bar
            Box(
                modifier = Modifier
                    .fillMaxWidth()
                    .padding(horizontal = 16.dp, vertical = 16.dp)
            ) {
                TextField(
                    value = searchQuery,
                    onValueChange = { searchQuery = it },
                    placeholder = { Text("Search by username to message...", color = Color.Gray) },
                    leadingIcon = { Icon(Icons.Default.Search, contentDescription = "Search", tint = Color.Gray) },
                    trailingIcon = { Icon(Icons.Default.Tune, contentDescription = "Filter", tint = Color.Gray) },
                    modifier = Modifier
                        .fillMaxWidth()
                        .border(1.dp, primaryRed.copy(alpha = 0.5f), RoundedCornerShape(24.dp))
                        .clip(RoundedCornerShape(24.dp)),
                    colors = TextFieldDefaults.colors(
                        focusedContainerColor = surfaceColor,
                        unfocusedContainerColor = surfaceColor,
                        focusedIndicatorColor = Color.Transparent,
                        unfocusedIndicatorColor = Color.Transparent,
                        focusedTextColor = Color.White,
                        unfocusedTextColor = Color.White
                    ),
                    singleLine = true
                )
            }
            
            // Stories Section
            Row(
                modifier = Modifier.fillMaxWidth().padding(horizontal = 16.dp),
                horizontalArrangement = Arrangement.SpaceBetween,
                verticalAlignment = Alignment.CenterVertically
            ) {
                Text("Stories", color = Color.White, fontSize = 18.sp, fontWeight = FontWeight.Bold)
                Text("View all", color = primaryRed, fontSize = 14.sp, fontWeight = FontWeight.Medium)
            }
            
            Spacer(modifier = Modifier.height(16.dp))
            
            LazyRow(
                contentPadding = PaddingValues(horizontal = 16.dp),
                horizontalArrangement = Arrangement.spacedBy(16.dp)
            ) {
                // Add Story
                item {
                    Column(horizontalAlignment = Alignment.CenterHorizontally) {
                        Box(
                            modifier = Modifier
                                .size(64.dp)
                                .border(1.dp, primaryRed, CircleShape),
                            contentAlignment = Alignment.Center
                        ) {
                            Icon(Icons.Default.Add, contentDescription = "Add Story", tint = primaryRed, modifier = Modifier.size(32.dp))
                        }
                        Spacer(modifier = Modifier.height(8.dp))
                        Text("Add Story", color = Color.White, fontSize = 12.sp)
                    }
                }
                // Mock Stories
                items(stories) { story ->
                    Column(horizontalAlignment = Alignment.CenterHorizontally) {
                        Box {
                            Box(
                                modifier = Modifier
                                    .size(64.dp)
                                    .clip(CircleShape)
                                    .background(Color.DarkGray)
                                    .border(2.dp, primaryRed, CircleShape),
                                contentAlignment = Alignment.Center
                            ) {
                                Text(story.name.take(1).uppercase(), color = Color.White, fontSize = 24.sp, fontWeight = FontWeight.Bold)
                            }
                            // Online indicator
                            Box(
                                modifier = Modifier
                                    .size(16.dp)
                                    .align(Alignment.BottomEnd)
                                    .offset(x = (-2).dp, y = (-2).dp)
                                    .clip(CircleShape)
                                    .background(if (story.isOnline) Color(0xFF4CAF50) else Color.Gray)
                                    .border(2.dp, bgColor, CircleShape)
                            )
                        }
                        Spacer(modifier = Modifier.height(8.dp))
                        Text(story.name, color = Color.White, fontSize = 12.sp)
                    }
                }
            }
            
            Spacer(modifier = Modifier.height(24.dp))
            
            // Filter Chips container
            Box(
                modifier = Modifier
                    .fillMaxSize()
                    .clip(RoundedCornerShape(topStart = 24.dp, topEnd = 24.dp))
                    .background(surfaceColor)
            ) {
                Column {
                    // Filter Chips Row
                    LazyRow(
                        modifier = Modifier.padding(top = 16.dp, bottom = 8.dp),
                        contentPadding = PaddingValues(horizontal = 16.dp),
                        horizontalArrangement = Arrangement.spacedBy(8.dp)
                    ) {
                        item { FilterChip(text = "All Messages", selected = true) }
                        item { FilterChipWithBadge(text = "Unread", badgeCount = 2, selected = false) }
                        item { FilterChip(text = "Groups", selected = false) }
                        item { FilterChip(text = "Requests", selected = false) }
                    }
                    
                    // Chat List
                    LazyColumn(
                        contentPadding = PaddingValues(horizontal = 16.dp, vertical = 8.dp),
                        verticalArrangement = Arrangement.spacedBy(12.dp)
                    ) {
                        items(chats) { chat ->
                            ChatListItem(chat = chat)
                        }
                        item { Spacer(modifier = Modifier.height(80.dp)) }
                    }
                }
            }
        }
    }
}

@Composable
fun FilterChip(text: String, selected: Boolean) {
    Box(
        modifier = Modifier
            .clip(RoundedCornerShape(20.dp))
            .background(if (selected) Color(0xFFE50914) else Color(0xFF2C2C2E))
            .padding(horizontal = 16.dp, vertical = 8.dp)
            .clickable { /* TODO */ }
    ) {
        Text(text, color = Color.White, fontSize = 14.sp, fontWeight = FontWeight.Medium)
    }
}

@Composable
fun FilterChipWithBadge(text: String, badgeCount: Int, selected: Boolean) {
    Row(
        modifier = Modifier
            .clip(RoundedCornerShape(20.dp))
            .background(if (selected) Color(0xFFE50914) else Color(0xFF2C2C2E))
            .padding(horizontal = 16.dp, vertical = 8.dp)
            .clickable { /* TODO */ },
        verticalAlignment = Alignment.CenterVertically
    ) {
        Text(text, color = Color.White, fontSize = 14.sp, fontWeight = FontWeight.Medium)
        if (badgeCount > 0) {
            Spacer(modifier = Modifier.width(6.dp))
            Box(
                modifier = Modifier
                    .size(20.dp)
                    .clip(CircleShape)
                    .background(Color(0xFFE50914)),
                contentAlignment = Alignment.Center
            ) {
                Text(badgeCount.toString(), color = Color.White, fontSize = 12.sp, fontWeight = FontWeight.Bold)
            }
        }
    }
}

@Composable
fun ChatListItem(chat: SocialScreenChatMock) {
    val bgColor = Color(0xFF1C1C1E) // matches the surface container
    Row(
        modifier = Modifier
            .fillMaxWidth()
            .clip(RoundedCornerShape(16.dp))
            .background(Color(0xFF121212)) // Darker background for each item inside surface
            .clickable { /* open chat */ }
            .padding(12.dp),
        verticalAlignment = Alignment.CenterVertically
    ) {
        // Avatar
        Box {
            Box(
                modifier = Modifier
                    .size(56.dp)
                    .clip(CircleShape)
                    .background(Color(0xFF2C2C2E)),
                contentAlignment = Alignment.Center
            ) {
                if (chat.isGroup) {
                    Icon(painterResource(android.R.drawable.ic_menu_myplaces), contentDescription = null, tint = Color.White)
                } else {
                    Text(chat.name.take(1).uppercase(), color = Color.White, fontSize = 20.sp, fontWeight = FontWeight.Bold)
                }
            }
            // Online dot
            Box(
                modifier = Modifier
                    .size(14.dp)
                    .align(Alignment.BottomEnd)
                    .offset(x = (-2).dp, y = (-2).dp)
                    .clip(CircleShape)
                    .background(if (chat.isOnline) Color(0xFF4CAF50) else Color.Gray)
                    .border(2.dp, Color(0xFF121212), CircleShape)
            )
        }
        
        Spacer(modifier = Modifier.width(16.dp))
        
        // Texts
        Column(modifier = Modifier.weight(1f)) {
            Text(chat.name, color = Color.White, fontSize = 16.sp, fontWeight = FontWeight.SemiBold)
            Spacer(modifier = Modifier.height(4.dp))
            Text(chat.message, color = Color.Gray, fontSize = 14.sp, maxLines = 1)
        }
        
        // Time & Badge
        Column(horizontalAlignment = Alignment.End) {
            Text(chat.time, color = if (chat.unread > 0) Color(0xFFE50914) else Color.Gray, fontSize = 12.sp)
            Spacer(modifier = Modifier.height(6.dp))
            if (chat.unread > 0) {
                Box(
                    modifier = Modifier
                        .size(24.dp)
                        .clip(CircleShape)
                        .background(Color(0xFFE50914)),
                    contentAlignment = Alignment.Center
                ) {
                    Text(chat.unread.toString(), color = Color.White, fontSize = 12.sp, fontWeight = FontWeight.Bold)
                }
            } else {
                Icon(Icons.AutoMirrored.Filled.KeyboardArrowRight, contentDescription = null, tint = Color.Gray, modifier = Modifier.size(20.dp))
            }
        }
    }
}
