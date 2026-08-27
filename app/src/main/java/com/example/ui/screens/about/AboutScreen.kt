package com.example.ui.screens.about

import androidx.compose.foundation.background
import androidx.compose.foundation.border
import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.foundation.verticalScroll
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.ChevronRight
import androidx.compose.material.icons.outlined.ChatBubbleOutline
import androidx.compose.material.icons.outlined.Diamond
import androidx.compose.material.icons.outlined.FavoriteBorder
import androidx.compose.material.icons.outlined.Groups
import androidx.compose.material.icons.outlined.Lock
import androidx.compose.material.icons.outlined.Policy
import androidx.compose.material.icons.outlined.Verified
import androidx.compose.material3.*
import androidx.compose.runtime.Composable
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.layout.ContentScale
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import coil.compose.AsyncImage

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun AboutScreen(onBack: () -> Unit = {}) {
    val scrollState = rememberScrollState()

    Column(
        modifier = Modifier
            .fillMaxSize()
            .verticalScroll(scrollState)
            .padding(horizontal = 16.dp, vertical = 24.dp)
    ) {
        // Top section with logo and text
        Row(
            modifier = Modifier.fillMaxWidth(),
            horizontalArrangement = Arrangement.SpaceBetween,
            verticalAlignment = Alignment.Top
        ) {
            Column(modifier = Modifier.weight(0.6f)) {
                Text(
                    text = "About CineStream",
                    color = Color.White,
                    fontSize = 28.sp,
                    fontWeight = FontWeight.Bold
                )
                Spacer(modifier = Modifier.height(16.dp))
                Text(
                    text = "CineStream is your premium cinematic experience. Stream your favorite movies and series in high quality, anytime, anywhere.",
                    color = Color.LightGray,
                    fontSize = 14.sp,
                    lineHeight = 20.sp
                )
                Spacer(modifier = Modifier.height(16.dp))
                Box(modifier = Modifier.width(32.dp).height(2.dp).background(Color(0xFFE50914)))
                Spacer(modifier = Modifier.height(24.dp))
                
                // Version Chip
                Row(
                    modifier = Modifier
                        .clip(RoundedCornerShape(8.dp))
                        .background(Color(0xFF161618))
                        .border(1.dp, Color(0xFF2A2A2E), RoundedCornerShape(8.dp))
                        .padding(horizontal = 12.dp, vertical = 8.dp),
                    verticalAlignment = Alignment.CenterVertically
                ) {
                    Icon(Icons.Outlined.Verified, contentDescription = null, tint = Color(0xFFE50914), modifier = Modifier.size(16.dp))
                    Spacer(modifier = Modifier.width(8.dp))
                    Text("Version 1.0.0", color = Color.LightGray, fontSize = 12.sp)
                }
                Spacer(modifier = Modifier.height(8.dp))
                Text("Last updated: May 25, 2024", color = Color.Gray, fontSize = 12.sp)
            }

            // Logo Image placeholder
            Box(modifier = Modifier.weight(0.4f).padding(start = 16.dp), contentAlignment = Alignment.Center) {
                AsyncImage(
                    model = "https://images.unsplash.com/photo-1485846234645-a62644f84728?q=80&w=300&auto=format&fit=crop",
                    contentDescription = "Logo",
                    modifier = Modifier
                        .size(120.dp)
                        .clip(RoundedCornerShape(24.dp))
                        .border(1.dp, Color(0xFF2A2A2E), RoundedCornerShape(24.dp)),
                    contentScale = ContentScale.Crop,
                    alpha = 0.8f
                )
                // Red C placeholder
                Text("C", color = Color(0xFFE50914), fontSize = 60.sp, fontWeight = FontWeight.Black, fontFamily = androidx.compose.ui.text.font.FontFamily.Serif)
            }
        }

        Spacer(modifier = Modifier.height(32.dp))

        // Our Mission Card
        Box(
            modifier = Modifier
                .fillMaxWidth()
                .clip(RoundedCornerShape(16.dp))
                .background(Color(0xFF161618))
                .border(1.dp, Color(0xFF2A2A2E), RoundedCornerShape(16.dp))
                .padding(20.dp)
        ) {
            Row(horizontalArrangement = Arrangement.SpaceBetween, verticalAlignment = Alignment.CenterVertically) {
                Column(modifier = Modifier.weight(0.7f)) {
                    Row(verticalAlignment = Alignment.CenterVertically) {
                        // Target icon placeholder
                        Icon(Icons.Outlined.Verified, contentDescription = null, tint = Color(0xFFE50914))
                        Spacer(modifier = Modifier.width(8.dp))
                        Text("Our Mission", color = Color.White, fontSize = 18.sp, fontWeight = FontWeight.Bold)
                    }
                    Spacer(modifier = Modifier.height(12.dp))
                    Text(
                        "To deliver the best entertainment experience with a simple, fast and beautiful streaming platform.",
                        color = Color.LightGray,
                        fontSize = 14.sp,
                        lineHeight = 20.sp
                    )
                }
                // Placeholder image for director's chair
                AsyncImage(
                    model = "https://images.unsplash.com/photo-1594909122845-11baa439b7bf?q=80&w=200&auto=format&fit=crop",
                    contentDescription = null,
                    modifier = Modifier.size(80.dp).clip(RoundedCornerShape(12.dp)),
                    contentScale = ContentScale.Crop,
                    alpha = 0.6f
                )
            }
        }

        Spacer(modifier = Modifier.height(16.dp))

        // Features Grid
        Row(modifier = Modifier.fillMaxWidth(), horizontalArrangement = Arrangement.spacedBy(12.dp)) {
            FeatureCard(modifier = Modifier.weight(1f), icon = Icons.Outlined.Verified, title = "Reliable", subtitle = "Secure and stable streaming experience.")
            FeatureCard(modifier = Modifier.weight(1f), icon = Icons.Outlined.Verified, title = "Fast", subtitle = "Optimized performance for everyone.")
        }
        Spacer(modifier = Modifier.height(12.dp))
        Row(modifier = Modifier.fillMaxWidth(), horizontalArrangement = Arrangement.spacedBy(12.dp)) {
            FeatureCard(modifier = Modifier.weight(1f), icon = Icons.Outlined.Diamond, title = "Premium", subtitle = "High quality content and features.")
            FeatureCard(modifier = Modifier.weight(1f), icon = Icons.Outlined.FavoriteBorder, title = "Made for You", subtitle = "Designed to bring you the best.")
        }

        Spacer(modifier = Modifier.height(24.dp))

        // Links list
        Column(
            modifier = Modifier
                .fillMaxWidth()
                .clip(RoundedCornerShape(16.dp))
                .background(Color(0xFF161618))
                .border(1.dp, Color(0xFF2A2A2E), RoundedCornerShape(16.dp))
        ) {
            AboutLinkItem(icon = Icons.Outlined.Groups, title = "Meet the Team", isLast = false)
            AboutLinkItem(icon = Icons.Outlined.Policy, title = "Terms of Service", isLast = false)
            AboutLinkItem(icon = Icons.Outlined.Lock, title = "Privacy Policy", isLast = false)
            AboutLinkItem(icon = Icons.Outlined.ChatBubbleOutline, title = "Contact Us", isLast = true)
        }

        Spacer(modifier = Modifier.height(24.dp))

        Button(
            onClick = { },
            modifier = Modifier.fillMaxWidth().height(50.dp),
            colors = ButtonDefaults.buttonColors(containerColor = Color(0xFFE50914)),
            shape = RoundedCornerShape(12.dp)
        ) {
            Text("Check for Updates", fontSize = 16.sp, fontWeight = FontWeight.Bold, color = Color.White)
        }
        Spacer(modifier = Modifier.height(32.dp))
    }
}

@Composable
fun FeatureCard(modifier: Modifier = Modifier, icon: androidx.compose.ui.graphics.vector.ImageVector, title: String, subtitle: String) {
    Column(
        modifier = modifier
            .clip(RoundedCornerShape(16.dp))
            .background(Color(0xFF161618))
            .border(1.dp, Color(0xFF2A2A2E), RoundedCornerShape(16.dp))
            .padding(16.dp),
        horizontalAlignment = Alignment.CenterHorizontally
    ) {
        Icon(icon, contentDescription = null, tint = Color(0xFFE50914), modifier = Modifier.size(24.dp))
        Spacer(modifier = Modifier.height(12.dp))
        Text(title, color = Color.White, fontSize = 16.sp, fontWeight = FontWeight.Bold, textAlign = androidx.compose.ui.text.style.TextAlign.Center)
        Spacer(modifier = Modifier.height(8.dp))
        Text(subtitle, color = Color.Gray, fontSize = 12.sp, textAlign = androidx.compose.ui.text.style.TextAlign.Center, lineHeight = 16.sp)
    }
}

@Composable
fun AboutLinkItem(icon: androidx.compose.ui.graphics.vector.ImageVector, title: String, isLast: Boolean) {
    Row(
        modifier = Modifier
            .fillMaxWidth()
            .clickable { }
            .padding(horizontal = 16.dp, vertical = 16.dp),
        verticalAlignment = Alignment.CenterVertically
    ) {
        Icon(icon, contentDescription = null, tint = Color.Gray, modifier = Modifier.size(20.dp))
        Spacer(modifier = Modifier.width(16.dp))
        Text(title, color = Color.White, fontSize = 16.sp, modifier = Modifier.weight(1f))
        Icon(Icons.Default.ChevronRight, contentDescription = null, tint = Color.Gray)
    }
    if (!isLast) {
        Box(modifier = Modifier.fillMaxWidth().height(1.dp).background(Color(0xFF2A2A2E)))
    }
}
