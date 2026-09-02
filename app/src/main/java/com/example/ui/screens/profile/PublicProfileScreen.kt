package com.example.ui.screens.profile

import androidx.compose.foundation.background
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.shape.CircleShape
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.automirrored.filled.ArrowBack
import androidx.compose.material.icons.filled.Person
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
import coil.compose.AsyncImage
import com.example.data.repository.SocialRepository
import com.example.data.repository.UserProfile

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun PublicProfileScreen(userId: String, onBack: () -> Unit) {
    var userProfile by remember { mutableStateOf<UserProfile?>(null) }
    var isLoading by remember { mutableStateOf(true) }
    
    val bgColor = Color(0xFF121212)
    val surfaceColor = Color(0xFF1C1C1E)

    LaunchedEffect(userId) {
        val repo = SocialRepository()
        userProfile = repo.getUserProfile(userId)
        isLoading = false
    }

    Scaffold(
        topBar = {
            TopAppBar(
                title = { Text("Profile", color = Color.White) },
                navigationIcon = {
                    IconButton(onClick = onBack) {
                        Icon(Icons.AutoMirrored.Filled.ArrowBack, contentDescription = "Back", tint = Color.White)
                    }
                },
                colors = TopAppBarDefaults.topAppBarColors(containerColor = surfaceColor)
            )
        },
        containerColor = bgColor
    ) { padding ->
        Box(modifier = Modifier.fillMaxSize().padding(padding).background(bgColor)) {
            if (isLoading) {
                CircularProgressIndicator(modifier = Modifier.align(Alignment.Center), color = Color(0xFFE50914))
            } else if (userProfile == null) {
                Text("User not found", color = Color.White, modifier = Modifier.align(Alignment.Center))
            } else {
                Column(
                    modifier = Modifier.fillMaxWidth().padding(24.dp),
                    horizontalAlignment = Alignment.CenterHorizontally
                ) {
                    Box(
                        modifier = Modifier
                            .size(120.dp)
                            .clip(CircleShape)
                            .background(surfaceColor),
                        contentAlignment = Alignment.Center
                    ) {
                        if (userProfile!!.photoUrl.isNotEmpty()) {
                            AsyncImage(
                                model = userProfile!!.photoUrl,
                                contentDescription = "Avatar",
                                contentScale = ContentScale.Crop,
                                modifier = Modifier.fillMaxSize()
                            )
                        } else {
                            Text(
                                text = userProfile!!.displayName.take(1).uppercase(),
                                color = Color.White,
                                fontSize = 48.sp,
                                fontWeight = FontWeight.Bold
                            )
                        }
                    }
                    
                    Spacer(modifier = Modifier.height(16.dp))
                    
                    Text(
                        text = userProfile!!.displayName,
                        color = Color.White,
                        fontSize = 24.sp,
                        fontWeight = FontWeight.Bold
                    )
                    
                    if (userProfile!!.username.isNotBlank()) {
                        Text(
                            text = "@${userProfile!!.username}",
                            color = Color.Gray,
                            fontSize = 16.sp
                        )
                    }
                    
                    Spacer(modifier = Modifier.height(24.dp))
                    
                    if (!userProfile!!.isProfilePublic) {
                        Surface(
                            shape = RoundedCornerShape(12.dp),
                            color = surfaceColor,
                            modifier = Modifier.fillMaxWidth()
                        ) {
                            PaddingValues(16.dp)
                            Row(modifier = Modifier.padding(16.dp), verticalAlignment = Alignment.CenterVertically) {
                                Icon(Icons.Default.Person, contentDescription = null, tint = Color.Gray)
                                Spacer(modifier = Modifier.width(16.dp))
                                Text("This account is private.", color = Color.Gray)
                            }
                        }
                    } else {
                         Surface(
                            shape = RoundedCornerShape(12.dp),
                            color = surfaceColor,
                            modifier = Modifier.fillMaxWidth()
                        ) {
                            Column(modifier = Modifier.padding(16.dp)) {
                                Text("Bio", color = Color.Gray, fontSize = 14.sp)
                                Spacer(modifier = Modifier.height(8.dp))
                                Text("Hi, I'm using CineStream!", color = Color.White, fontSize = 16.sp)
                            }
                        }
                    }
                }
            }
        }
    }
}
