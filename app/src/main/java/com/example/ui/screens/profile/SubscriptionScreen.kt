package com.example.ui.screens.profile

import androidx.compose.foundation.background
import androidx.compose.foundation.border
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.foundation.verticalScroll
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.ArrowBack
import androidx.compose.material.icons.filled.CheckCircle
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun SubscriptionScreen(onBack: () -> Unit) {
    val primaryRed = Color(0xFFE50914)
    val bgColor = Color(0xFF121212)
    val cardColor = Color(0xFF1E1E1E)
    
    Scaffold(
        topBar = {
            TopAppBar(
                title = { Text("Subscription", color = Color.White) },
                navigationIcon = {
                    IconButton(onClick = onBack) {
                        Icon(Icons.Default.ArrowBack, contentDescription = "Back", tint = Color.White)
                    }
                },
                colors = TopAppBarDefaults.topAppBarColors(containerColor = bgColor)
            )
        },
        containerColor = bgColor
    ) { padding ->
        Column(
            modifier = Modifier
                .fillMaxSize()
                .padding(padding)
                .verticalScroll(rememberScrollState())
                .padding(24.dp)
        ) {
            Text("Choose Your Plan", color = Color.White, fontSize = 24.sp, fontWeight = FontWeight.Bold)
            Spacer(modifier = Modifier.height(8.dp))
            Text("Unlock unlimited access to all movies, series, and anime with a premium subscription.", color = Color.Gray, fontSize = 14.sp)
            Spacer(modifier = Modifier.height(32.dp))
            
            // Basic Plan
            PlanCard(
                title = "Basic",
                price = "Free",
                features = listOf("Ads supported", "SD Quality", "Limited downloads"),
                isCurrent = false,
                buttonText = "Current Plan",
                primaryRed = primaryRed,
                cardColor = cardColor
            )
            
            Spacer(modifier = Modifier.height(24.dp))
            
            // Premium Plan
            PlanCard(
                title = "Premium",
                price = "$9.99/mo",
                features = listOf("Ad-free streaming", "4K Ultra HD Quality", "Unlimited downloads", "Cancel anytime"),
                isCurrent = true,
                buttonText = "Manage Plan",
                primaryRed = primaryRed,
                cardColor = cardColor
            )
        }
    }
}

@Composable
fun PlanCard(title: String, price: String, features: List<String>, isCurrent: Boolean, buttonText: String, primaryRed: Color, cardColor: Color) {
    Column(
        modifier = Modifier
            .fillMaxWidth()
            .border(if (isCurrent) 2.dp else 0.dp, if (isCurrent) primaryRed else Color.Transparent, RoundedCornerShape(16.dp))
            .background(cardColor, RoundedCornerShape(16.dp))
            .padding(24.dp)
    ) {
        Row(modifier = Modifier.fillMaxWidth(), horizontalArrangement = Arrangement.SpaceBetween, verticalAlignment = Alignment.CenterVertically) {
            Text(title, color = Color.White, fontSize = 20.sp, fontWeight = FontWeight.Bold)
            if (isCurrent) {
                Box(modifier = Modifier.background(primaryRed.copy(alpha = 0.2f), RoundedCornerShape(4.dp)).padding(horizontal = 8.dp, vertical = 4.dp)) {
                    Text("ACTIVE", color = primaryRed, fontSize = 10.sp, fontWeight = FontWeight.Bold)
                }
            }
        }
        Spacer(modifier = Modifier.height(8.dp))
        Text(price, color = Color.White, fontSize = 32.sp, fontWeight = FontWeight.Bold)
        Spacer(modifier = Modifier.height(24.dp))
        
        features.forEach { feature ->
            Row(verticalAlignment = Alignment.CenterVertically) {
                Icon(Icons.Default.CheckCircle, contentDescription = null, tint = if (isCurrent) primaryRed else Color.Gray, modifier = Modifier.size(16.dp))
                Spacer(modifier = Modifier.width(12.dp))
                Text(feature, color = Color.White, fontSize = 14.sp)
            }
            Spacer(modifier = Modifier.height(12.dp))
        }
        
        Spacer(modifier = Modifier.height(16.dp))
        Button(
            onClick = {},
            modifier = Modifier.fillMaxWidth().height(48.dp),
            colors = ButtonDefaults.buttonColors(containerColor = if (isCurrent) primaryRed else Color(0xFF2C2C2E)),
            shape = RoundedCornerShape(12.dp)
        ) {
            Text(buttonText, color = Color.White, fontWeight = FontWeight.Bold)
        }
    }
}
