package com.example.ui.screens.settings

import androidx.compose.foundation.background
import androidx.compose.foundation.border
import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.shape.CircleShape
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.Check
import androidx.compose.material.icons.filled.ColorLens
import androidx.compose.material.icons.filled.Language
import androidx.compose.material.icons.filled.Palette
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
    var selectedTheme by remember { mutableStateOf("System") }
    var selectedLanguage by remember { mutableStateOf("English") }
    var selectedColor by remember { mutableStateOf(Color(0xFFE50914)) } // Red default

    val colors = listOf(
        Color(0xFFE50914), // Red
        Color(0xFF00A8FF), // Blue
        Color(0xFF4CAF50), // Green
        Color(0xFFFFC107), // Yellow
        Color(0xFF9C27B0)  // Purple
    )

    Column(
        modifier = Modifier
            .fillMaxSize()
            .padding(16.dp),
        horizontalAlignment = Alignment.Start
    ) {
        Text(
            text = "Settings / الإعدادات",
            style = MaterialTheme.typography.headlineMedium,
            fontWeight = FontWeight.Bold,
            color = Color.White,
            modifier = Modifier.padding(bottom = 24.dp, top = 16.dp)
        )

        // Theme Section
        SettingsSectionTitle(title = "Theme / المظهر", icon = Icons.Default.Palette)
        Row(
            modifier = Modifier.fillMaxWidth().padding(vertical = 8.dp),
            horizontalArrangement = Arrangement.spacedBy(12.dp)
        ) {
            ThemeOption("System", selectedTheme == "System") { selectedTheme = "System" }
            ThemeOption("Light", selectedTheme == "Light") { selectedTheme = "Light" }
            ThemeOption("Dark", selectedTheme == "Dark") { selectedTheme = "Dark" }
        }

        Spacer(modifier = Modifier.height(24.dp))

        // Language Section
        SettingsSectionTitle(title = "Language / اللغة", icon = Icons.Default.Language)
        Row(
            modifier = Modifier.fillMaxWidth().padding(vertical = 8.dp),
            horizontalArrangement = Arrangement.spacedBy(12.dp)
        ) {
            LanguageOption("English", selectedLanguage == "English") { selectedLanguage = "English" }
            LanguageOption("العربية", selectedLanguage == "العربية") { selectedLanguage = "العربية" }
        }

        Spacer(modifier = Modifier.height(24.dp))

        // Color Section
        SettingsSectionTitle(title = "Accent Color / لون التطبيق", icon = Icons.Default.ColorLens)
        Row(
            modifier = Modifier.fillMaxWidth().padding(vertical = 12.dp),
            horizontalArrangement = Arrangement.spacedBy(16.dp)
        ) {
            colors.forEach { color ->
                ColorOption(color, isSelected = selectedColor == color) {
                    selectedColor = color
                }
            }
        }
    }
}

@Composable
fun SettingsSectionTitle(title: String, icon: androidx.compose.ui.graphics.vector.ImageVector) {
    Row(verticalAlignment = Alignment.CenterVertically) {
        Icon(icon, contentDescription = null, tint = Color.LightGray, modifier = Modifier.size(20.dp))
        Spacer(modifier = Modifier.width(8.dp))
        Text(text = title, style = MaterialTheme.typography.titleMedium, color = Color.LightGray, fontWeight = FontWeight.SemiBold)
    }
}

@Composable
fun RowScope.ThemeOption(title: String, isSelected: Boolean, onClick: () -> Unit) {
    Box(
        modifier = Modifier
            .weight(1f)
            .clip(RoundedCornerShape(8.dp))
            .background(if (isSelected) MaterialTheme.colorScheme.primary else Color(0xFF2A2A2E))
            .clickable { onClick() }
            .padding(vertical = 12.dp),
        contentAlignment = Alignment.Center
    ) {
        Text(title, color = if (isSelected) Color.White else Color.Gray, fontWeight = FontWeight.Medium)
    }
}

@Composable
fun RowScope.LanguageOption(title: String, isSelected: Boolean, onClick: () -> Unit) {
    Box(
        modifier = Modifier
            .weight(1f)
            .clip(RoundedCornerShape(8.dp))
            .background(if (isSelected) MaterialTheme.colorScheme.primary else Color(0xFF2A2A2E))
            .clickable { onClick() }
            .padding(vertical = 12.dp),
        contentAlignment = Alignment.Center
    ) {
        Text(title, color = if (isSelected) Color.White else Color.Gray, fontWeight = FontWeight.Medium)
    }
}

@Composable
fun ColorOption(color: Color, isSelected: Boolean, onClick: () -> Unit) {
    Box(
        modifier = Modifier
            .size(48.dp)
            .clip(CircleShape)
            .background(color)
            .border(
                width = if (isSelected) 3.dp else 0.dp,
                color = if (isSelected) Color.White else Color.Transparent,
                shape = CircleShape
            )
            .clickable { onClick() },
        contentAlignment = Alignment.Center
    ) {
        if (isSelected) {
            Icon(Icons.Default.Check, contentDescription = "Selected", tint = Color.White)
        }
    }
}
