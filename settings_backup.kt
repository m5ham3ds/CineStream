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
import androidx.compose.material.icons.outlined.Home
import androidx.compose.material.icons.outlined.Language
import androidx.compose.material.icons.outlined.LightMode
import androidx.compose.material.icons.outlined.Palette
import androidx.compose.material.icons.outlined.Settings
import androidx.compose.material.icons.outlined.PlayCircleOutline
import androidx.compose.material.icons.outlined.Download
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.res.stringResource
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import com.example.R
import com.example.data.repository.UserPreferencesRepository
import com.example.ui.theme.PrimaryBlue
import com.example.ui.theme.PrimaryGreen
import com.example.ui.theme.PrimaryPurple
import com.example.ui.theme.PrimaryRed
import com.example.ui.theme.PrimaryYellow
import kotlinx.coroutines.launch

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun SettingsScreen() {
    val context = LocalContext.current
    val userPrefs = remember { UserPreferencesRepository(context) }
    val coroutineScope = rememberCoroutineScope()
    
    val themeMode by userPrefs.themeMode.collectAsState(initial = 0)
    val primaryColor by userPrefs.primaryColor.collectAsState(initial = 0)
    val appLanguage by userPrefs.appLanguage.collectAsState(initial = "system")
    val startScreen by userPrefs.startScreen.collectAsState(initial = "home")
    
    val scrollState = rememberScrollState()
    
    // Bottom Sheets State
    var showLanguageSheet by remember { mutableStateOf(false) }
    var showStartScreenSheet by remember { mutableStateOf(false) }

    val currentThemeName = when(themeMode) {
        1 -> stringResource(R.string.light)
        2 -> stringResource(R.string.dark)
        else -> stringResource(R.string.system)
    }

    val currentColorName = when(primaryColor) {
        1 -> stringResource(R.string.blue)
        2 -> stringResource(R.string.green)
        3 -> stringResource(R.string.purple)
        4 -> stringResource(R.string.yellow)
        else -> stringResource(R.string.red)
    }

    val currentLanguageName = when(appLanguage) {
        "en" -> stringResource(R.string.english)
        "ar" -> stringResource(R.string.arabic)
        else -> stringResource(R.string.system)
    }

    val currentStartScreenName = when(startScreen) {
        "search" -> stringResource(R.string.search)
        "downloads" -> stringResource(R.string.downloads)
        "settings" -> stringResource(R.string.settings)
        else -> stringResource(R.string.home)
    }

    Column(
        modifier = Modifier
            .fillMaxSize()
            .background(MaterialTheme.colorScheme.background)
            .verticalScroll(scrollState)
            .padding(horizontal = 16.dp, vertical = 8.dp)
    ) {
        // Appearance Section
        SettingsSectionHeader(icon = Icons.Outlined.Palette, title = stringResource(R.string.appearance))
        Column(
            modifier = Modifier
                .fillMaxWidth()
                .clip(RoundedCornerShape(16.dp))
                .background(MaterialTheme.colorScheme.surface)
                .border(1.dp, MaterialTheme.colorScheme.surfaceVariant, RoundedCornerShape(16.dp))
        ) {
            // Theme Mode
            Row(
                modifier = Modifier
                    .fillMaxWidth()
                    .padding(horizontal = 16.dp, vertical = 16.dp),
                verticalAlignment = Alignment.CenterVertically,
                horizontalArrangement = Arrangement.SpaceBetween
            ) {
                Row(verticalAlignment = Alignment.CenterVertically) {
                    Box(modifier = Modifier.size(40.dp).clip(CircleShape).border(1.dp, MaterialTheme.colorScheme.surfaceVariant, CircleShape), contentAlignment = Alignment.Center) {
                        Icon(Icons.Outlined.Settings, contentDescription = null, tint = MaterialTheme.colorScheme.onSurfaceVariant, modifier = Modifier.size(20.dp))
                    }
                    Spacer(modifier = Modifier.width(16.dp))
                    Column {
                        Text(stringResource(R.string.theme), color = MaterialTheme.colorScheme.onSurface, fontSize = 16.sp, fontWeight = FontWeight.SemiBold)
                        Text(currentThemeName, color = MaterialTheme.colorScheme.onSurfaceVariant, fontSize = 12.sp)
                    }
                }
                
                // Theme selector
                Row(
                    modifier = Modifier
                        .clip(RoundedCornerShape(percent = 50))
                        .background(MaterialTheme.colorScheme.surfaceVariant)
                        .padding(4.dp),
                    verticalAlignment = Alignment.CenterVertically
                ) {
                    Box(modifier = Modifier.clip(CircleShape).background(if(themeMode == 0) MaterialTheme.colorScheme.primary else Color.Transparent).clickable { coroutineScope.launch { userPrefs.saveThemeMode(0) } }.padding(8.dp)) {
                        Icon(Icons.Outlined.Settings, contentDescription = "System", tint = if(themeMode == 0) Color.White else MaterialTheme.colorScheme.onSurfaceVariant, modifier = Modifier.size(16.dp))
                    }
                    Spacer(modifier = Modifier.width(4.dp))
                    Box(modifier = Modifier.clip(CircleShape).background(if(themeMode == 1) MaterialTheme.colorScheme.primary else Color.Transparent).clickable { coroutineScope.launch { userPrefs.saveThemeMode(1) } }.padding(8.dp)) {
                        Icon(Icons.Outlined.LightMode, contentDescription = "Light", tint = if(themeMode == 1) Color.White else MaterialTheme.colorScheme.onSurfaceVariant, modifier = Modifier.size(16.dp))
                    }
                    Spacer(modifier = Modifier.width(4.dp))
                    Box(modifier = Modifier.clip(CircleShape).background(if(themeMode == 2) MaterialTheme.colorScheme.primary else Color.Transparent).clickable { coroutineScope.launch { userPrefs.saveThemeMode(2) } }.padding(8.dp)) {
                        Icon(Icons.Outlined.DarkMode, contentDescription = "Dark", tint = if(themeMode == 2) Color.White else MaterialTheme.colorScheme.onSurfaceVariant, modifier = Modifier.size(16.dp))
                    }
                }
            }
            
            Box(modifier = Modifier.fillMaxWidth().height(1.dp).background(MaterialTheme.colorScheme.surfaceVariant))
            
            // Accent Color Row
            Row(
                modifier = Modifier.fillMaxWidth().padding(horizontal = 16.dp, vertical = 16.dp),
                verticalAlignment = Alignment.CenterVertically,
                horizontalArrangement = Arrangement.SpaceBetween
            ) {
                Row(verticalAlignment = Alignment.CenterVertically) {
                    Box(modifier = Modifier.size(40.dp).clip(CircleShape).border(1.dp, MaterialTheme.colorScheme.surfaceVariant, CircleShape), contentAlignment = Alignment.Center) {
                        Icon(Icons.Outlined.ColorLens, contentDescription = null, tint = MaterialTheme.colorScheme.onSurfaceVariant, modifier = Modifier.size(20.dp))
                    }
                    Spacer(modifier = Modifier.width(16.dp))
                    Column {
                        Text(stringResource(R.string.accent_color), color = MaterialTheme.colorScheme.onSurface, fontSize = 16.sp, fontWeight = FontWeight.SemiBold)
                        Text(currentColorName, color = MaterialTheme.colorScheme.onSurfaceVariant, fontSize = 12.sp)
                    }
                }
                
                // Color selector
                Row(horizontalArrangement = Arrangement.spacedBy(8.dp)) {
                    ColorCircle(color = PrimaryRed, isSelected = primaryColor == 0, onClick = { coroutineScope.launch { userPrefs.savePrimaryColor(0) } })
                    ColorCircle(color = PrimaryBlue, isSelected = primaryColor == 1, onClick = { coroutineScope.launch { userPrefs.savePrimaryColor(1) } })
                    ColorCircle(color = PrimaryGreen, isSelected = primaryColor == 2, onClick = { coroutineScope.launch { userPrefs.savePrimaryColor(2) } })
                    ColorCircle(color = PrimaryPurple, isSelected = primaryColor == 3, onClick = { coroutineScope.launch { userPrefs.savePrimaryColor(3) } })
                    ColorCircle(color = PrimaryYellow, isSelected = primaryColor == 4, onClick = { coroutineScope.launch { userPrefs.savePrimaryColor(4) } })
                }
            }
        }
        
        Spacer(modifier = Modifier.height(24.dp))
        
        // General Section
        SettingsSectionHeader(icon = Icons.Outlined.Settings, title = stringResource(R.string.general))
        Column(
            modifier = Modifier
                .fillMaxWidth()
                .clip(RoundedCornerShape(16.dp))
                .background(MaterialTheme.colorScheme.surface)
                .border(1.dp, MaterialTheme.colorScheme.surfaceVariant, RoundedCornerShape(16.dp))
        ) {
            SettingsListItem(
                icon = Icons.Outlined.Language, 
                title = stringResource(R.string.language), 
                subtitle = currentLanguageName, 
                isLast = false,
                onClick = { showLanguageSheet = true }
            )
            SettingsListItem(
                icon = Icons.Outlined.Home, 
                title = stringResource(R.string.start_screen), 
                subtitle = currentStartScreenName, 
                isLast = true,
                onClick = { showStartScreenSheet = true }
            )
        }
        
        Spacer(modifier = Modifier.height(100.dp))
    }

    // Language Selection Sheet
    if (showLanguageSheet) {
        ModalBottomSheet(onDismissRequest = { showLanguageSheet = false }) {
            Column(modifier = Modifier.fillMaxWidth().padding(16.dp)) {
                Text(stringResource(R.string.language), style = MaterialTheme.typography.titleLarge, modifier = Modifier.padding(bottom = 16.dp))
                
                ListItem(
                    headlineContent = { Text(stringResource(R.string.system)) },
                    modifier = Modifier.clickable { coroutineScope.launch { userPrefs.saveAppLanguage("system"); showLanguageSheet = false } }
                )
                ListItem(
                    headlineContent = { Text(stringResource(R.string.english)) },
                    modifier = Modifier.clickable { coroutineScope.launch { userPrefs.saveAppLanguage("en"); showLanguageSheet = false } }
                )
                ListItem(
                    headlineContent = { Text(stringResource(R.string.arabic)) },
                    modifier = Modifier.clickable { coroutineScope.launch { userPrefs.saveAppLanguage("ar"); showLanguageSheet = false } }
                )
                Spacer(modifier = Modifier.height(32.dp))
            }
        }
    }

    // Start Screen Selection Sheet
    if (showStartScreenSheet) {
        ModalBottomSheet(onDismissRequest = { showStartScreenSheet = false }) {
            Column(modifier = Modifier.fillMaxWidth().padding(16.dp)) {
                Text(stringResource(R.string.start_screen), style = MaterialTheme.typography.titleLarge, modifier = Modifier.padding(bottom = 16.dp))
                
                ListItem(
                    headlineContent = { Text(stringResource(R.string.home)) },
                    modifier = Modifier.clickable { coroutineScope.launch { userPrefs.saveStartScreen("home"); showStartScreenSheet = false } }
                )
                ListItem(
                    headlineContent = { Text(stringResource(R.string.search)) },
                    modifier = Modifier.clickable { coroutineScope.launch { userPrefs.saveStartScreen("search"); showStartScreenSheet = false } }
                )
                ListItem(
                    headlineContent = { Text(stringResource(R.string.downloads)) },
                    modifier = Modifier.clickable { coroutineScope.launch { userPrefs.saveStartScreen("downloads"); showStartScreenSheet = false } }
                )
                ListItem(
                    headlineContent = { Text(stringResource(R.string.settings)) },
                    modifier = Modifier.clickable { coroutineScope.launch { userPrefs.saveStartScreen("settings"); showStartScreenSheet = false } }
                )
                Spacer(modifier = Modifier.height(32.dp))
            }
        }
    }
}

@Composable
fun SettingsSectionHeader(icon: androidx.compose.ui.graphics.vector.ImageVector, title: String) {
    Row(verticalAlignment = Alignment.CenterVertically, modifier = Modifier.padding(bottom = 12.dp)) {
        Icon(icon, contentDescription = null, tint = MaterialTheme.colorScheme.primary, modifier = Modifier.size(20.dp))
        Spacer(modifier = Modifier.width(8.dp))
        Text(title, color = MaterialTheme.colorScheme.onBackground, fontSize = 16.sp, fontWeight = FontWeight.Bold)
    }
}

@Composable
fun ColorCircle(color: Color, isSelected: Boolean, onClick: () -> Unit) {
    Box(
        modifier = Modifier
            .size(24.dp)
            .clip(CircleShape)
            .background(color)
            .clickable { onClick() }
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
fun SettingsListItem(
    icon: androidx.compose.ui.graphics.vector.ImageVector, 
    title: String, 
    subtitle: String, 
    isLast: Boolean,
    onClick: () -> Unit
) {
    Row(
        modifier = Modifier
            .fillMaxWidth()
            .clickable { onClick() }
            .padding(horizontal = 16.dp, vertical = 16.dp),
        verticalAlignment = Alignment.CenterVertically
    ) {
        Box(modifier = Modifier.size(40.dp).clip(CircleShape).border(1.dp, MaterialTheme.colorScheme.surfaceVariant, CircleShape), contentAlignment = Alignment.Center) {
            Icon(icon, contentDescription = null, tint = MaterialTheme.colorScheme.onSurfaceVariant, modifier = Modifier.size(20.dp))
        }
        Spacer(modifier = Modifier.width(16.dp))
        Column(modifier = Modifier.weight(1f)) {
            Text(title, color = MaterialTheme.colorScheme.onSurface, fontSize = 16.sp, fontWeight = FontWeight.SemiBold)
            Spacer(modifier = Modifier.height(2.dp))
            Text(subtitle, color = MaterialTheme.colorScheme.onSurfaceVariant, fontSize = 12.sp)
        }
        Icon(Icons.Default.ChevronRight, contentDescription = null, tint = MaterialTheme.colorScheme.onSurfaceVariant)
    }
    if (!isLast) {
        Box(modifier = Modifier.fillMaxWidth().height(1.dp).background(MaterialTheme.colorScheme.surfaceVariant))
    }
}
