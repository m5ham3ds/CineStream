package com.example.ui.screens.settings

import androidx.compose.foundation.background
import androidx.compose.foundation.border
import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.shape.CircleShape
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.foundation.verticalScroll
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.Check
import androidx.compose.material.icons.filled.ChevronRight
import androidx.compose.material.icons.outlined.ColorLens
import androidx.compose.material.icons.outlined.DarkMode
import androidx.compose.material.icons.outlined.Download
import androidx.compose.material.icons.outlined.Home
import androidx.compose.material.icons.outlined.Language
import androidx.compose.material.icons.outlined.LightMode
import androidx.compose.material.icons.outlined.Notifications
import androidx.compose.material.icons.outlined.Palette
import androidx.compose.material.icons.outlined.PlayCircleOutline
import androidx.compose.material.icons.outlined.Settings
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp

@Composable
fun SettingsScreen() {
    var pushNotifications by remember { mutableStateOf(true) }
    val scrollState = rememberScrollState()

    Column(
        modifier = Modifier
            .fillMaxSize()
            .verticalScroll(scrollState)
            .padding(horizontal = 16.dp, vertical = 8.dp)
    ) {
        
        // Appearance Section
        SettingsSectionHeader(icon = Icons.Outlined.Palette, title = "Appearance")
        Column(
            modifier = Modifier
                .fillMaxWidth()
                .clip(RoundedCornerShape(16.dp))
                .background(Color(0xFF161618))
                .border(1.dp, Color(0xFF2A2A2E), RoundedCornerShape(16.dp))
        ) {
            // Theme Row
            Row(
                modifier = Modifier.fillMaxWidth().padding(horizontal = 16.dp, vertical = 16.dp),
                verticalAlignment = Alignment.CenterVertically,
                horizontalArrangement = Arrangement.SpaceBetween
            ) {
                Row(verticalAlignment = Alignment.CenterVertically) {
                    Box(modifier = Modifier.size(40.dp).clip(CircleShape).border(1.dp, Color(0xFF2A2A2E), CircleShape), contentAlignment = Alignment.Center) {
                        Icon(Icons.Outlined.Settings, contentDescription = null, tint = Color.LightGray, modifier = Modifier.size(20.dp))
                    }
                    Spacer(modifier = Modifier.width(16.dp))
                    Column {
                        Text("Theme", color = Color.White, fontSize = 16.sp, fontWeight = FontWeight.SemiBold)
                        Text("System", color = Color.Gray, fontSize = 12.sp)
                    }
                }
                
                // Theme selector
                Row(
                    modifier = Modifier
                        .clip(RoundedCornerShape(percent = 50))
                        .background(Color(0xFF2A2A2E))
                        .padding(4.dp),
                    verticalAlignment = Alignment.CenterVertically
                ) {
                    Box(modifier = Modifier.clip(CircleShape).background(Color(0xFFE50914)).padding(8.dp)) {
                        Icon(Icons.Outlined.Settings, contentDescription = "System", tint = Color.White, modifier = Modifier.size(16.dp))
                    }
                    Spacer(modifier = Modifier.width(4.dp))
                    Box(modifier = Modifier.clip(CircleShape).padding(8.dp)) {
                        Icon(Icons.Outlined.LightMode, contentDescription = "Light", tint = Color.Gray, modifier = Modifier.size(16.dp))
                    }
                    Spacer(modifier = Modifier.width(4.dp))
                    Box(modifier = Modifier.clip(CircleShape).padding(8.dp)) {
                        Icon(Icons.Outlined.DarkMode, contentDescription = "Dark", tint = Color.Gray, modifier = Modifier.size(16.dp))
                    }
                }
            }
            
            Box(modifier = Modifier.fillMaxWidth().height(1.dp).background(Color(0xFF2A2A2E)))
            
            // Accent Color Row
            Row(
                modifier = Modifier.fillMaxWidth().padding(horizontal = 16.dp, vertical = 16.dp),
                verticalAlignment = Alignment.CenterVertically,
                horizontalArrangement = Arrangement.SpaceBetween
            ) {
                Row(verticalAlignment = Alignment.CenterVertically) {
                    Box(modifier = Modifier.size(40.dp).clip(CircleShape).border(1.dp, Color(0xFF2A2A2E), CircleShape), contentAlignment = Alignment.Center) {
                        Icon(Icons.Outlined.ColorLens, contentDescription = null, tint = Color.LightGray, modifier = Modifier.size(20.dp))
                    }
                    Spacer(modifier = Modifier.width(16.dp))
                    Column {
                        Text("Accent Color", color = Color.White, fontSize = 16.sp, fontWeight = FontWeight.SemiBold)
                        Text("Red", color = Color.Gray, fontSize = 12.sp)
                    }
                }
                
                // Color selector
                Row(horizontalArrangement = Arrangement.spacedBy(8.dp)) {
                    ColorCircle(color = Color(0xFFE50914), isSelected = true)
                    ColorCircle(color = Color(0xFF00A8FF), isSelected = false)
                    ColorCircle(color = Color(0xFF4CAF50), isSelected = false)
                    ColorCircle(color = Color(0xFFFFC107), isSelected = false)
                    ColorCircle(color = Color(0xFF9C27B0), isSelected = false)
                }
            }
        }

        Spacer(modifier = Modifier.height(24.dp))
        
        // General Section
        SettingsSectionHeader(icon = Icons.Outlined.Settings, title = "General")
        Column(
            modifier = Modifier
                .fillMaxWidth()
                .clip(RoundedCornerShape(16.dp))
                .background(Color(0xFF161618))
                .border(1.dp, Color(0xFF2A2A2E), RoundedCornerShape(16.dp))
        ) {
            SettingsListItem(icon = Icons.Outlined.Language, title = "Language", subtitle = "English", isLast = false)
            SettingsListItem(icon = Icons.Outlined.Home, title = "Default Home", subtitle = "Home", isLast = false)
            SettingsListItem(icon = Icons.Outlined.PlayCircleOutline, title = "Playback Settings", subtitle = "Quality, Subtitles, Auto play...", isLast = false)
            SettingsListItem(icon = Icons.Outlined.Download, title = "Downloads", subtitle = "Quality, Location, Storage", isLast = true)
        }

        Spacer(modifier = Modifier.height(24.dp))

        // Notifications Section
        SettingsSectionHeader(icon = Icons.Outlined.Notifications, title = "Notifications")
        Column(
            modifier = Modifier
                .fillMaxWidth()
                .clip(RoundedCornerShape(16.dp))
                .background(Color(0xFF161618))
                .border(1.dp, Color(0xFF2A2A2E), RoundedCornerShape(16.dp))
        ) {
            Row(
                modifier = Modifier
                    .fillMaxWidth()
                    .clickable { pushNotifications = !pushNotifications }
                    .padding(horizontal = 16.dp, vertical = 16.dp),
                verticalAlignment = Alignment.CenterVertically
            ) {
                Box(modifier = Modifier.size(40.dp).clip(CircleShape).border(1.dp, Color(0xFF2A2A2E), CircleShape), contentAlignment = Alignment.Center) {
                    Icon(Icons.Outlined.Notifications, contentDescription = null, tint = Color.LightGray, modifier = Modifier.size(20.dp))
                }
                Spacer(modifier = Modifier.width(16.dp))
                Column(modifier = Modifier.weight(1f)) {
                    Text("Push Notifications", color = Color.White, fontSize = 16.sp, fontWeight = FontWeight.SemiBold)
                    Text("Receive updates and alerts", color = Color.Gray, fontSize = 12.sp)
                }
                Switch(
                    checked = pushNotifications,
                    onCheckedChange = { pushNotifications = it },
                    colors = SwitchDefaults.colors(
                        checkedThumbColor = Color.White,
                        checkedTrackColor = Color(0xFFE50914),
                        uncheckedThumbColor = Color.LightGray,
                        uncheckedTrackColor = Color(0xFF2A2A2E),
                        uncheckedBorderColor = Color.Transparent
                    )
                )
            }
        }
        
        Spacer(modifier = Modifier.height(100.dp))
    }
}

@Composable
fun SettingsSectionHeader(icon: androidx.compose.ui.graphics.vector.ImageVector, title: String) {
    Row(verticalAlignment = Alignment.CenterVertically, modifier = Modifier.padding(bottom = 12.dp)) {
        Icon(icon, contentDescription = null, tint = Color(0xFFE50914), modifier = Modifier.size(20.dp))
        Spacer(modifier = Modifier.width(8.dp))
        Text(title, color = Color.White, fontSize = 16.sp, fontWeight = FontWeight.Bold)
    }
}

@Composable
fun ColorCircle(color: Color, isSelected: Boolean) {
    Box(
        modifier = Modifier
            .size(24.dp)
            .clip(CircleShape)
            .background(color)
            .border(
                width = if (isSelected) 2.dp else 0.dp,
                color = if (isSelected) Color.White else Color.Transparent,
                shape = CircleShape
            ),
        contentAlignment = Alignment.Center
    ) {
        if (isSelected) {
            Icon(Icons.Default.Check, contentDescription = null, tint = Color.White, modifier = Modifier.size(14.dp))
        }
    }
}

@Composable
fun SettingsListItem(icon: androidx.compose.ui.graphics.vector.ImageVector, title: String, subtitle: String, isLast: Boolean) {
    Row(
        modifier = Modifier
            .fillMaxWidth()
            .clickable { }
            .padding(horizontal = 16.dp, vertical = 16.dp),
        verticalAlignment = Alignment.CenterVertically
    ) {
        Box(modifier = Modifier.size(40.dp).clip(CircleShape).border(1.dp, Color(0xFF2A2A2E), CircleShape), contentAlignment = Alignment.Center) {
            Icon(icon, contentDescription = null, tint = Color.LightGray, modifier = Modifier.size(20.dp))
        }
        Spacer(modifier = Modifier.width(16.dp))
        Column(modifier = Modifier.weight(1f)) {
            Text(title, color = Color.White, fontSize = 16.sp, fontWeight = FontWeight.SemiBold)
            Spacer(modifier = Modifier.height(2.dp))
            Text(subtitle, color = Color.Gray, fontSize = 12.sp)
        }
        Icon(Icons.Default.ChevronRight, contentDescription = null, tint = Color.Gray)
    }
    if (!isLast) {
        Box(modifier = Modifier.fillMaxWidth().height(1.dp).background(Color(0xFF2A2A2E)))
    }
}
