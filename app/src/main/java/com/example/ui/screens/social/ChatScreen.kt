package com.example.ui.screens.social

import androidx.compose.foundation.background
import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items
import androidx.compose.foundation.shape.CircleShape
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.foundation.text.BasicTextField
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.automirrored.filled.ArrowBack
import androidx.compose.material.icons.automirrored.filled.Send
import androidx.compose.material.icons.filled.*
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.graphics.SolidColor
import androidx.compose.ui.layout.ContentScale
import androidx.compose.ui.text.TextStyle
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import coil.compose.AsyncImage
import java.text.SimpleDateFormat
import java.util.Date
import java.util.Locale

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun ChatScreen(
    conversationId: String,
    viewModel: ChatViewModel = androidx.lifecycle.viewmodel.compose.viewModel(),
    onBack: () -> Unit,
    onUserClick: (String) -> Unit = {}
) {
    val currentUser by viewModel.currentUser.collectAsState()
    val otherUser by viewModel.otherUser.collectAsState()
    val messages by viewModel.messages.collectAsState()
    var messageText by remember { mutableStateOf("") }
    
    val bgColor = Color(0xFF121212)
    val surfaceColor = Color(0xFF1C1C1E)
    val primaryRed = Color(0xFFE50914)
    val darkGray = Color(0xFF2C2C2E)

    LaunchedEffect(conversationId) {
        viewModel.loadConversation(conversationId)
    }

    Scaffold(
        topBar = {
            TopAppBar(
                title = { 
                    Row(
                        verticalAlignment = Alignment.CenterVertically,
                        modifier = Modifier
                            .clickable { otherUser?.uid?.let { onUserClick(it) } }
                            .padding(vertical = 4.dp, horizontal = 4.dp)
                    ) {
                        Box(
                            modifier = Modifier.size(40.dp).clip(CircleShape).background(darkGray),
                            contentAlignment = Alignment.Center
                        ) {
                            if (otherUser?.photoUrl?.isNotEmpty() == true) {
                                AsyncImage(
                                    model = otherUser?.photoUrl,
                                    contentDescription = null,
                                    contentScale = ContentScale.Crop,
                                    modifier = Modifier.fillMaxSize()
                                )
                            } else {
                                Text((otherUser?.displayName?.take(1) ?: "U").uppercase(), color = Color.White, fontWeight = FontWeight.Bold)
                            }
                            
                            // Online indicator
                            Box(
                                modifier = Modifier
                                    .size(12.dp)
                                    .align(Alignment.BottomEnd)
                                    .background(bgColor, CircleShape)
                                    .padding(2.dp)
                            ) {
                                Box(modifier = Modifier.fillMaxSize().background(Color(0xFF4CAF50), CircleShape))
                            }
                        }
                        Spacer(modifier = Modifier.width(12.dp))
                        Column {
                            Text(otherUser?.displayName ?: "Loading...", color = Color.White, fontSize = 16.sp, fontWeight = FontWeight.Bold)
                            Row(verticalAlignment = Alignment.CenterVertically) {
                                Box(modifier = Modifier.size(6.dp).background(primaryRed, CircleShape))
                                Spacer(modifier = Modifier.width(4.dp))
                                Text("Online", color = Color.LightGray, fontSize = 12.sp)
                            }
                        }
                    }
                },
                navigationIcon = {
                    IconButton(onClick = onBack) {
                        Icon(Icons.AutoMirrored.Filled.ArrowBack, contentDescription = "Back", tint = Color.White)
                    }
                },
                actions = {
                    IconButton(onClick = {}) { Icon(Icons.Default.Phone, contentDescription = "Call", tint = primaryRed) }
                    IconButton(onClick = {}) { Icon(Icons.Default.Search, contentDescription = "Search", tint = primaryRed) }
                    IconButton(onClick = {}) { Icon(Icons.Default.MoreVert, contentDescription = "More", tint = Color.White) }
                },
                colors = TopAppBarDefaults.topAppBarColors(containerColor = bgColor)
            )
        },
        bottomBar = {
            Box(
                modifier = Modifier
                    .fillMaxWidth()
                    .background(bgColor)
                    .padding(horizontal = 16.dp, vertical = 12.dp)
            ) {
                Row(
                    modifier = Modifier.fillMaxWidth().background(surfaceColor, RoundedCornerShape(32.dp)).padding(6.dp),
                    verticalAlignment = Alignment.CenterVertically
                ) {
                    Box(
                        modifier = Modifier
                            .size(44.dp)
                            .clip(RoundedCornerShape(16.dp))
                            .background(darkGray)
                            .clickable { },
                        contentAlignment = Alignment.Center
                    ) {
                        Icon(Icons.Default.AttachFile, contentDescription = "Attach", tint = primaryRed, modifier = Modifier.size(24.dp))
                    }
                    
                    Spacer(modifier = Modifier.width(8.dp))
                    
                    Box(modifier = Modifier.weight(1f)) {
                        if (messageText.isEmpty()) {
                            Text("Type a message...", color = Color.Gray, fontSize = 16.sp)
                        }
                        BasicTextField(
                            value = messageText,
                            onValueChange = { messageText = it },
                            textStyle = TextStyle(color = Color.White, fontSize = 16.sp),
                            cursorBrush = SolidColor(primaryRed),
                            modifier = Modifier.fillMaxWidth()
                        )
                    }
                    
                    Icon(Icons.Default.Face, contentDescription = "Emoji", tint = primaryRed, modifier = Modifier.size(24.dp))
                    
                    Spacer(modifier = Modifier.width(12.dp))
                    
                    Box(
                        modifier = Modifier
                            .size(48.dp)
                            .clip(CircleShape)
                            .background(primaryRed)
                            .clickable {
                                viewModel.sendMessage(messageText)
                                messageText = ""
                            },
                        contentAlignment = Alignment.Center
                    ) {
                        Icon(Icons.AutoMirrored.Filled.Send, contentDescription = "Send", tint = Color.White)
                    }
                }
            }
        },
        containerColor = bgColor
    ) { padding ->
        LazyColumn(
            modifier = Modifier
                .fillMaxSize()
                .padding(padding),
            contentPadding = PaddingValues(16.dp),
            reverseLayout = true
        ) {
            items(messages.reversed()) { msg ->
                val isMe = msg.senderId == currentUser?.uid
                Row(
                    modifier = Modifier
                        .fillMaxWidth()
                        .padding(vertical = 4.dp),
                    horizontalArrangement = if (isMe) Arrangement.End else Arrangement.Start
                ) {
                    Column(
                        horizontalAlignment = if (isMe) Alignment.End else Alignment.Start
                    ) {
                        Box(
                            modifier = Modifier
                                .background(
                                    color = if (isMe) primaryRed else darkGray,
                                    shape = RoundedCornerShape(
                                        topStart = 20.dp,
                                        topEnd = 20.dp,
                                        bottomStart = if (isMe) 20.dp else 4.dp,
                                        bottomEnd = if (isMe) 4.dp else 20.dp
                                    )
                                )
                                .padding(horizontal = 16.dp, vertical = 10.dp)
                        ) {
                            Text(text = msg.text, color = Color.White, fontSize = 15.sp)
                        }
                        
                        val sdf = SimpleDateFormat("hh:mm a", Locale.getDefault())
                        Row(verticalAlignment = Alignment.CenterVertically, modifier = Modifier.padding(top = 4.dp)) {
                            Text(sdf.format(Date(msg.timestamp)), fontSize = 11.sp, color = Color.Gray)
                            if (isMe) {
                                Spacer(modifier = Modifier.width(4.dp))
                                Icon(Icons.Default.DoneAll, contentDescription = "Read", tint = primaryRed, modifier = Modifier.size(14.dp))
                            }
                        }
                    }
                }
            }
            
            item {
                Column(
                    modifier = Modifier.fillMaxWidth().padding(vertical = 16.dp),
                    horizontalAlignment = Alignment.CenterHorizontally
                ) {
                    Box(
                        modifier = Modifier
                            .background(surfaceColor, RoundedCornerShape(16.dp))
                            .padding(horizontal = 12.dp, vertical = 12.dp)
                    ) {
                        Row(verticalAlignment = Alignment.CenterVertically) {
                            Icon(Icons.Default.Security, contentDescription = "Encrypted", tint = primaryRed, modifier = Modifier.size(20.dp))
                            Spacer(modifier = Modifier.width(8.dp))
                            Text("Messages are end-to-end encrypted.\nYour privacy is our priority.", color = Color.LightGray, fontSize = 12.sp, lineHeight = 16.sp)
                        }
                    }
                    
                    Spacer(modifier = Modifier.height(16.dp))
                    
                    Box(
                        modifier = Modifier
                            .background(surfaceColor, RoundedCornerShape(16.dp))
                            .padding(horizontal = 12.dp, vertical = 4.dp)
                    ) {
                        Text("Today", color = Color.White, fontSize = 12.sp)
                    }
                }
            }
        }
    }
}
