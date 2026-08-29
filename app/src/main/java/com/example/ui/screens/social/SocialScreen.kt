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
import androidx.compose.material.icons.automirrored.filled.Send
import androidx.compose.material.icons.filled.Add
import androidx.compose.material.icons.filled.PersonAdd
import androidx.compose.material.icons.filled.Search
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import com.example.data.repository.DownloadRepository
import com.example.data.repository.LibraryRepository
import kotlinx.coroutines.launch

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun SocialScreen(onBack: () -> Unit) {
    val context = LocalContext.current
    val downloadRepository = remember { DownloadRepository(context) }
    val libraryRepository = remember { LibraryRepository(context) }
    
    val downloads by downloadRepository.getDownloadItems().collectAsState(initial = emptyList())
    val library by libraryRepository.getLibraryItems().collectAsState(initial = emptyList())
    
    var searchQuery by remember { mutableStateOf("") }
    val friends = remember { mutableStateListOf("Ahmed", "Sara", "Ali") }
    var showAddStoryDialog by remember { mutableStateOf(false) }
    
    // Fake stories for now
    val stories = remember { mutableStateListOf("Ahmed", "Sara") }

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
                placeholder = { Text("Search by username to message...") },
                leadingIcon = { Icon(Icons.Default.Search, contentDescription = null) },
                trailingIcon = { 
                    if (searchQuery.isNotEmpty()) {
                        IconButton(onClick = { 
                            if (!friends.contains(searchQuery)) friends.add(0, searchQuery)
                            searchQuery = "" 
                        }) {
                            Icon(Icons.Default.PersonAdd, contentDescription = "Add Friend")
                        }
                    }
                },
                shape = RoundedCornerShape(12.dp),
                colors = OutlinedTextFieldDefaults.colors(
                    unfocusedContainerColor = MaterialTheme.colorScheme.surface,
                    focusedContainerColor = MaterialTheme.colorScheme.surface
                )
            )

            // Stories
            Text(
                "Stories", 
                fontWeight = FontWeight.Bold, 
                fontSize = 18.sp, 
                color = MaterialTheme.colorScheme.onBackground,
                modifier = Modifier.padding(horizontal = 16.dp, vertical = 8.dp)
            )
            
            LazyRow(
                contentPadding = PaddingValues(horizontal = 16.dp),
                horizontalArrangement = Arrangement.spacedBy(12.dp)
            ) {
                // Add Story Button
                item {
                    Column(horizontalAlignment = Alignment.CenterHorizontally) {
                        Box(
                            modifier = Modifier
                                .size(64.dp)
                                .clip(CircleShape)
                                .background(MaterialTheme.colorScheme.surfaceVariant)
                                .border(2.dp, MaterialTheme.colorScheme.primary, CircleShape)
                                .clickable { showAddStoryDialog = true },
                            contentAlignment = Alignment.Center
                        ) {
                            Icon(Icons.Default.Add, contentDescription = "Add Story", tint = MaterialTheme.colorScheme.primary)
                        }
                        Spacer(modifier = Modifier.height(4.dp))
                        Text("Add Story", fontSize = 12.sp, color = MaterialTheme.colorScheme.onBackground)
                    }
                }
                
                items(stories) { user ->
                    Column(horizontalAlignment = Alignment.CenterHorizontally) {
                        Box(
                            modifier = Modifier
                                .size(64.dp)
                                .clip(CircleShape)
                                .background(Color.DarkGray)
                                .border(2.dp, MaterialTheme.colorScheme.secondary, CircleShape),
                            contentAlignment = Alignment.Center
                        ) {
                            Text(user.take(1), fontSize = 24.sp, color = Color.White)
                        }
                        Spacer(modifier = Modifier.height(4.dp))
                        Text(user, fontSize = 12.sp, color = MaterialTheme.colorScheme.onBackground)
                    }
                }
            }

            Spacer(modifier = Modifier.height(16.dp))
            HorizontalDivider(color = MaterialTheme.colorScheme.surfaceVariant)
            
            // Messages List
            Text(
                "Messages", 
                fontWeight = FontWeight.Bold, 
                fontSize = 18.sp, 
                color = MaterialTheme.colorScheme.onBackground,
                modifier = Modifier.padding(horizontal = 16.dp, vertical = 16.dp)
            )
            
            LazyColumn(
                contentPadding = PaddingValues(bottom = 100.dp)
            ) {
                items(friends) { friend ->
                    Row(
                        modifier = Modifier
                            .fillMaxWidth()
                            .clickable { /* Open Chat (Placeholder) */ }
                            .padding(horizontal = 16.dp, vertical = 12.dp),
                        verticalAlignment = Alignment.CenterVertically
                    ) {
                        Box(
                            modifier = Modifier
                                .size(48.dp)
                                .clip(CircleShape)
                                .background(Color.Gray),
                            contentAlignment = Alignment.Center
                        ) {
                            Text(friend.take(1), fontSize = 20.sp, color = Color.White)
                        }
                        Spacer(modifier = Modifier.width(16.dp))
                        Column(modifier = Modifier.weight(1f)) {
                            Text(friend, fontWeight = FontWeight.Bold, color = MaterialTheme.colorScheme.onBackground)
                            Text("Tap to chat...", fontSize = 14.sp, color = MaterialTheme.colorScheme.onSurfaceVariant)
                        }
                        Icon(Icons.AutoMirrored.Filled.Send, contentDescription = null, tint = MaterialTheme.colorScheme.primary, modifier = Modifier.size(20.dp))
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
                    
                    val availableMedia = (downloads.map { it.title } + library.map { it.title }).distinct()
                    
                    LazyColumn(modifier = Modifier.fillMaxWidth().heightIn(max = 300.dp)) {
                        if (availableMedia.isEmpty()) {
                            item { Text("No media found in library or downloads.", color = MaterialTheme.colorScheme.error) }
                        }
                        items(availableMedia) { title ->
                            Text(
                                text = title,
                                modifier = Modifier
                                    .fillMaxWidth()
                                    .clickable {
                                        stories.add(0, "You")
                                        showAddStoryDialog = false
                                    }
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
