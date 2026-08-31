package com.example.ui.screens.social

import androidx.compose.foundation.background
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items
import androidx.compose.foundation.shape.CircleShape
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.automirrored.filled.ArrowBack
import androidx.compose.material.icons.filled.Send
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import java.text.SimpleDateFormat
import java.util.Date
import java.util.Locale

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun ChatScreen(
    conversationId: String,
    viewModel: ChatViewModel = androidx.lifecycle.viewmodel.compose.viewModel(),
    onBack: () -> Unit
) {
    val currentUser by viewModel.currentUser.collectAsState()
    val messages by viewModel.messages.collectAsState()
    var messageText by remember { mutableStateOf("") }
    
    val bgColor = Color(0xFF121212)
    val primaryRed = Color(0xFFE50914)

    LaunchedEffect(conversationId) {
        viewModel.loadConversation(conversationId)
    }

    Scaffold(
        topBar = {
            TopAppBar(
                title = { Text("Chat", color = Color.White) },
                navigationIcon = {
                    IconButton(onClick = onBack) {
                        Icon(Icons.AutoMirrored.Filled.ArrowBack, contentDescription = "Back", tint = Color.White)
                    }
                },
                colors = TopAppBarDefaults.topAppBarColors(
                    containerColor = Color(0xFF1C1C1E)
                )
            )
        },
        bottomBar = {
            Row(
                modifier = Modifier
                    .fillMaxWidth()
                    .background(Color(0xFF1C1C1E))
                    .padding(16.dp),
                verticalAlignment = Alignment.CenterVertically
            ) {
                OutlinedTextField(
                    value = messageText,
                    onValueChange = { messageText = it },
                    modifier = Modifier.weight(1f),
                    placeholder = { Text("Type a message...", color = Color.Gray) },
                    shape = RoundedCornerShape(24.dp),
                    colors = OutlinedTextFieldDefaults.colors(
                        focusedContainerColor = Color(0xFF2C2C2E),
                        unfocusedContainerColor = Color(0xFF2C2C2E),
                        focusedBorderColor = Color.Transparent,
                        unfocusedBorderColor = Color.Transparent,
                        focusedTextColor = Color.White,
                        unfocusedTextColor = Color.White
                    )
                )
                Spacer(modifier = Modifier.width(8.dp))
                IconButton(
                    onClick = { 
                        viewModel.sendMessage(messageText)
                        messageText = ""
                    },
                    modifier = Modifier
                        .size(48.dp)
                        .background(primaryRed, CircleShape)
                ) {
                    Icon(Icons.Default.Send, contentDescription = "Send", tint = Color.White)
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
            items(messages) { msg ->
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
                                    color = if (isMe) primaryRed else Color(0xFF2C2C2E),
                                    shape = RoundedCornerShape(
                                        topStart = 16.dp,
                                        topEnd = 16.dp,
                                        bottomStart = if (isMe) 16.dp else 4.dp,
                                        bottomEnd = if (isMe) 4.dp else 16.dp
                                    )
                                )
                                .padding(12.dp)
                        ) {
                            Text(
                                text = msg.text,
                                color = Color.White,
                                fontSize = 14.sp
                            )
                        }
                        val sdf = SimpleDateFormat("hh:mm a", Locale.getDefault())
                        Text(sdf.format(Date(msg.timestamp)), fontSize = 10.sp, color = Color.Gray, modifier = Modifier.padding(top = 2.dp, start = 4.dp, end = 4.dp))
                    }
                }
            }
        }
    }
}
