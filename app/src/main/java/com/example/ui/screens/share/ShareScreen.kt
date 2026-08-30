package com.example.ui.screens.share

import android.Manifest
import android.os.Build
import androidx.compose.foundation.background
import androidx.compose.foundation.border
import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items
import androidx.compose.foundation.shape.CircleShape
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.automirrored.filled.ArrowBack
import androidx.compose.material.icons.automirrored.filled.ArrowForward
import androidx.compose.material.icons.filled.*
import androidx.compose.material.icons.outlined.Info
import androidx.compose.material.icons.outlined.Movie
import androidx.compose.material.icons.outlined.Tv
import androidx.compose.material.icons.outlined.Folder
import androidx.compose.material.icons.outlined.Shield
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.graphics.vector.ImageVector
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.style.TextAlign
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import com.example.data.repository.DownloadRepository
import com.example.utils.P2PManager
import com.example.utils.P2PState
import com.google.accompanist.permissions.ExperimentalPermissionsApi
import com.google.accompanist.permissions.rememberMultiplePermissionsState
import java.io.File
import androidx.compose.foundation.lazy.LazyRow

@OptIn(ExperimentalPermissionsApi::class, ExperimentalMaterial3Api::class)
@Composable
fun ShareScreen(
    onBack: () -> Unit
) {
    val context = LocalContext.current
    val p2pManager = remember { P2PManager(context) }
    val downloadRepository = remember { com.example.data.repository.DownloadRepository(context) }
    val p2pState by p2pManager.p2pState.collectAsState()
    val connectedEndpoint by p2pManager.connectedEndpoint.collectAsState()
    val discoveredEndpoints by p2pManager.discoveredEndpoints.collectAsState()
    val transferProgress by p2pManager.transferProgress.collectAsState()
    
    val allDownloads by downloadRepository.getDownloadItems().collectAsState(initial = emptyList())
    val completedDownloads = remember(allDownloads) { allDownloads.filter { it.isCompleted } }


    DisposableEffect(Unit) {
        onDispose { p2pManager.stopAll() }
    }

    val permissions = if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.S) {
        listOf(
            Manifest.permission.BLUETOOTH_SCAN,
            Manifest.permission.BLUETOOTH_ADVERTISE,
            Manifest.permission.BLUETOOTH_CONNECT,
            Manifest.permission.ACCESS_FINE_LOCATION,
            Manifest.permission.NEARBY_WIFI_DEVICES
        )
    } else {
        listOf(
            Manifest.permission.BLUETOOTH,
            Manifest.permission.BLUETOOTH_ADMIN,
            Manifest.permission.ACCESS_FINE_LOCATION,
            Manifest.permission.ACCESS_COARSE_LOCATION
        )
    }

    val permissionsState = rememberMultiplePermissionsState(permissions)
    var showSendDialog by remember { mutableStateOf(false) }

    Scaffold(

        containerColor = MaterialTheme.colorScheme.background
    ) { padding ->


        LazyColumn(
            modifier = Modifier
                .fillMaxSize()
                .padding(padding)
                .padding(horizontal = 16.dp),
            contentPadding = PaddingValues(bottom = 24.dp)
        ) {
            // Connection Status
            item {
                Card(
                    modifier = Modifier.fillMaxWidth().padding(vertical = 8.dp),
                    shape = RoundedCornerShape(16.dp),
                    colors = CardDefaults.cardColors(containerColor = MaterialTheme.colorScheme.surfaceVariant.copy(alpha = 0.3f)),
                    border = borderStroke()
                ) {
                    Row(
                        modifier = Modifier.padding(16.dp).fillMaxWidth(),
                        verticalAlignment = Alignment.CenterVertically
                    ) {
                        Box(
                            modifier = Modifier
                                .size(56.dp)
                                .clip(CircleShape)
                                .background(Color.Red.copy(alpha = 0.1f))
                                .border(1.dp, Color.Red.copy(alpha = 0.3f), CircleShape),
                            contentAlignment = Alignment.Center
                        ) {
                            Icon(Icons.Default.Wifi, contentDescription = null, tint = Color.Red, modifier = Modifier.size(28.dp))
                        }
                        Spacer(modifier = Modifier.width(16.dp))
                        Column(modifier = Modifier.weight(1f)) {
                            Text("Connection Status", color = MaterialTheme.colorScheme.onSurfaceVariant, fontSize = 12.sp)
                            Text(p2pState.name, color = Color.Red, fontWeight = FontWeight.Bold, fontSize = 18.sp)
                            Text(
                                text = when (p2pState) {
                                    P2PState.IDLE -> "Waiting for action"
                                    P2PState.DISCOVERING -> "Looking for devices..."
                                    P2PState.ADVERTISING -> "Waiting to be discovered..."
                                    P2PState.CONNECTED -> "Connected to ${connectedEndpoint?.name}"
                                    P2PState.TRANSFERRING -> "Transferring... ${(transferProgress * 100).toInt()}%"
                                },
                                color = MaterialTheme.colorScheme.onSurfaceVariant,
                                fontSize = 12.sp
                            )
                        }
                        Surface(
                            shape = RoundedCornerShape(20.dp),
                            color = Color.Transparent,
                            border = borderStroke()
                        ) {
                            Row(modifier = Modifier.padding(horizontal = 12.dp, vertical = 6.dp), verticalAlignment = Alignment.CenterVertically) {
                                Text("How it works?", fontSize = 10.sp, color = MaterialTheme.colorScheme.onSurfaceVariant)
                                Spacer(modifier = Modifier.width(4.dp))
                                Icon(Icons.Outlined.Info, contentDescription = null, modifier = Modifier.size(12.dp), tint = MaterialTheme.colorScheme.onSurfaceVariant)
                            }
                        }
                    }
                }
            }

            // Actions
            item {
                Row(
                    modifier = Modifier.fillMaxWidth().padding(vertical = 8.dp),
                    horizontalArrangement = Arrangement.spacedBy(12.dp)
                ) {
                    // Send Card
                    Card(
                        modifier = Modifier.weight(1f).clickable { p2pManager.startDiscovery() },
                        shape = RoundedCornerShape(16.dp),
                        colors = CardDefaults.cardColors(containerColor = MaterialTheme.colorScheme.primary)
                    ) {
                        Row(modifier = Modifier.padding(16.dp), verticalAlignment = Alignment.CenterVertically) {
                            Box(
                                modifier = Modifier.size(40.dp).clip(CircleShape).background(Color.White.copy(alpha = 0.2f)),
                                contentAlignment = Alignment.Center
                            ) {
                                Icon(Icons.Default.Send, contentDescription = null, tint = Color.White)
                            }
                            Spacer(modifier = Modifier.width(12.dp))
                            Column(modifier = Modifier.weight(1f)) {
                                Text("Send Content", color = Color.White, fontWeight = FontWeight.Bold)
                                Text("Share movies, series\nor anime", color = Color.White.copy(alpha = 0.8f), fontSize = 11.sp, lineHeight = 14.sp)
                            }
                            Icon(Icons.AutoMirrored.Filled.ArrowForward, contentDescription = null, tint = Color.White)
                        }
                    }

                    // Receive Card
                    Card(
                        modifier = Modifier.weight(1f).clickable { p2pManager.startAdvertising(android.os.Build.MODEL) },
                        shape = RoundedCornerShape(16.dp),
                        colors = CardDefaults.cardColors(containerColor = MaterialTheme.colorScheme.surfaceVariant.copy(alpha = 0.5f)),
                        border = borderStroke()
                    ) {
                        Row(modifier = Modifier.padding(16.dp), verticalAlignment = Alignment.CenterVertically) {
                            Box(
                                modifier = Modifier.size(40.dp).clip(CircleShape).background(MaterialTheme.colorScheme.primary.copy(alpha = 0.1f)),
                                contentAlignment = Alignment.Center
                            ) {
                                Icon(Icons.Default.Download, contentDescription = null, tint = MaterialTheme.colorScheme.primary)
                            }
                            Spacer(modifier = Modifier.width(12.dp))
                            Column(modifier = Modifier.weight(1f)) {
                                Text("Receive Content", color = MaterialTheme.colorScheme.onBackground, fontWeight = FontWeight.Bold)
                                Text("Receive from nearby\ndevices", color = MaterialTheme.colorScheme.onSurfaceVariant, fontSize = 11.sp, lineHeight = 14.sp)
                            }
                            Icon(Icons.AutoMirrored.Filled.ArrowForward, contentDescription = null, tint = MaterialTheme.colorScheme.onSurfaceVariant)
                        }
                    }
                }
            }

            // Choose Content Type
            item {
                Spacer(modifier = Modifier.height(16.dp))
                Text("Choose Content Type", color = MaterialTheme.colorScheme.onBackground, fontSize = 18.sp, fontWeight = FontWeight.Bold)
                Spacer(modifier = Modifier.height(12.dp))
                
                Row(modifier = Modifier.fillMaxWidth(), horizontalArrangement = Arrangement.spacedBy(8.dp)) {
                    ContentTypeItem("Movies", Icons.Outlined.Movie, true, modifier = Modifier.weight(1f))
                    ContentTypeItem("TV Series", Icons.Outlined.Tv, false, modifier = Modifier.weight(1f))
                    ContentTypeItem("Anime", Icons.Default.Face, false, modifier = Modifier.weight(1f))
                    ContentTypeItem("All Files", Icons.Outlined.Folder, false, modifier = Modifier.weight(1f))
                }
            }

            // Recent Transfers
            item {
                Spacer(modifier = Modifier.height(24.dp))
                Row(modifier = Modifier.fillMaxWidth(), horizontalArrangement = Arrangement.SpaceBetween, verticalAlignment = Alignment.CenterVertically) {
                    Text("Recent Transfers", color = MaterialTheme.colorScheme.onBackground, fontSize = 18.sp, fontWeight = FontWeight.Bold)
                    Text("View All", color = MaterialTheme.colorScheme.primary, fontSize = 14.sp, fontWeight = FontWeight.Bold, modifier = Modifier.clickable { })
                }
                Spacer(modifier = Modifier.height(12.dp))
                
                // Static dummy items matching design
                RecentTransferItem(
                    title = "John Wick 4",
                    typeAndSize = "Movie • 2.1 GB",
                    status = "Sent",
                    target = "To: Ahmed's Phone",
                    time = "12:45 PM",
                    isSent = true,
                    completed = true
                )
                HorizontalDivider(color = MaterialTheme.colorScheme.surfaceVariant.copy(alpha = 0.5f))
                RecentTransferItem(
                    title = "Attack on Titan S4",
                    typeAndSize = "TV Series • 8.7 GB",
                    status = "Received",
                    target = "From: Sara's Phone",
                    time = "Yesterday",
                    isSent = false,
                    completed = true
                )
            }

            // Nearby Devices
            item {
                Spacer(modifier = Modifier.height(24.dp))
                Row(modifier = Modifier.fillMaxWidth(), horizontalArrangement = Arrangement.SpaceBetween, verticalAlignment = Alignment.CenterVertically) {
                    Text("Nearby Devices", color = MaterialTheme.colorScheme.onBackground, fontSize = 18.sp, fontWeight = FontWeight.Bold)
                    Row(verticalAlignment = Alignment.CenterVertically, modifier = Modifier.clickable { p2pManager.startDiscovery() }) {
                        Icon(Icons.Default.Refresh, contentDescription = null, tint = MaterialTheme.colorScheme.primary, modifier = Modifier.size(16.dp))
                        Spacer(modifier = Modifier.width(4.dp))
                        Text("Scan", color = MaterialTheme.colorScheme.primary, fontSize = 14.sp, fontWeight = FontWeight.Bold)
                    }
                }
                Spacer(modifier = Modifier.height(12.dp))
            }

            if (discoveredEndpoints.isEmpty() && p2pState != P2PState.DISCOVERING && p2pState != P2PState.CONNECTED) {
                item {
                    Text("No nearby devices found. Tap Scan to search.", color = MaterialTheme.colorScheme.onSurfaceVariant, fontSize = 14.sp, modifier = Modifier.padding(vertical = 16.dp))
                }
            } else if (discoveredEndpoints.isEmpty() && p2pState == P2PState.DISCOVERING) {
                item {
                    Row(modifier = Modifier.padding(vertical = 16.dp), verticalAlignment = Alignment.CenterVertically) {
                        CircularProgressIndicator(modifier = Modifier.size(24.dp), color = MaterialTheme.colorScheme.primary, strokeWidth = 2.dp)
                        Spacer(modifier = Modifier.width(12.dp))
                        Text("Searching for nearby devices...", color = MaterialTheme.colorScheme.onSurfaceVariant, fontSize = 14.sp)
                    }
                }
            }

            items(discoveredEndpoints) { endpoint ->
                Card(
                    modifier = Modifier.fillMaxWidth().padding(vertical = 6.dp),
                    shape = RoundedCornerShape(12.dp),
                    colors = CardDefaults.cardColors(containerColor = MaterialTheme.colorScheme.surfaceVariant.copy(alpha = 0.3f)),
                    border = borderStroke()
                ) {
                    Row(modifier = Modifier.padding(16.dp), verticalAlignment = Alignment.CenterVertically) {
                        Box(
                            modifier = Modifier.size(48.dp).clip(CircleShape).background(MaterialTheme.colorScheme.surfaceVariant),
                            contentAlignment = Alignment.Center
                        ) {
                            Icon(Icons.Default.Smartphone, contentDescription = null, tint = MaterialTheme.colorScheme.primary)
                        }
                        Spacer(modifier = Modifier.width(16.dp))
                        Column(modifier = Modifier.weight(1f)) {
                            Text(endpoint.name, color = MaterialTheme.colorScheme.onBackground, fontWeight = FontWeight.Bold, fontSize = 16.sp)
                            Text("Android • Ready to connect", color = MaterialTheme.colorScheme.onSurfaceVariant, fontSize = 12.sp)
                        }
                        Icon(Icons.Default.SignalCellularAlt, contentDescription = null, tint = Color.Green, modifier = Modifier.size(20.dp))
                        Spacer(modifier = Modifier.width(12.dp))
                        Button(
                            onClick = { p2pManager.requestConnection(endpoint.id, android.os.Build.MODEL) },
                            colors = ButtonDefaults.buttonColors(containerColor = MaterialTheme.colorScheme.primary.copy(alpha = 0.2f), contentColor = MaterialTheme.colorScheme.primary),
                            shape = RoundedCornerShape(8.dp),
                            contentPadding = PaddingValues(horizontal = 16.dp, vertical = 8.dp),
                            modifier = Modifier.height(36.dp)
                        ) {
                            Text("Connect", fontSize = 12.sp, fontWeight = FontWeight.Bold)
                        }
                    }
                }
            }

            // Connected Device
            if (p2pState == P2PState.CONNECTED && connectedEndpoint != null) {
                item {
                    Card(
                        modifier = Modifier.fillMaxWidth().padding(vertical = 6.dp),
                        shape = RoundedCornerShape(12.dp),
                        colors = CardDefaults.cardColors(containerColor = MaterialTheme.colorScheme.primary.copy(alpha = 0.1f)),
                        border = borderStroke()
                    ) {
                        Row(modifier = Modifier.padding(16.dp), verticalAlignment = Alignment.CenterVertically) {
                            Box(
                                modifier = Modifier.size(48.dp).clip(CircleShape).background(MaterialTheme.colorScheme.primary),
                                contentAlignment = Alignment.Center
                            ) {
                                Icon(Icons.Default.Smartphone, contentDescription = null, tint = Color.White)
                            }
                            Spacer(modifier = Modifier.width(16.dp))
                            Column(modifier = Modifier.weight(1f)) {
                                Text(connectedEndpoint!!.name, color = MaterialTheme.colorScheme.onBackground, fontWeight = FontWeight.Bold, fontSize = 16.sp)
                                Text("Connected", color = MaterialTheme.colorScheme.primary, fontSize = 12.sp)
                            }
                            Button(
                                onClick = { showSendDialog = true },
                                colors = ButtonDefaults.buttonColors(containerColor = MaterialTheme.colorScheme.primary),
                                shape = RoundedCornerShape(8.dp),
                                contentPadding = PaddingValues(horizontal = 16.dp, vertical = 8.dp),
                                modifier = Modifier.height(36.dp)
                            ) {
                                Text("Select File", fontSize = 12.sp, fontWeight = FontWeight.Bold)
                            }
                        }
                    }
                }
            }

            // Transfer Progress
            if (p2pState == P2PState.TRANSFERRING) {
                item {
                    Column(modifier = Modifier.fillMaxWidth().padding(vertical = 12.dp)) {
                        Text("Transferring File...", color = MaterialTheme.colorScheme.onBackground, fontWeight = FontWeight.Bold, fontSize = 14.sp)
                        Spacer(modifier = Modifier.height(8.dp))
                        LinearProgressIndicator(
                            progress = { transferProgress },
                            modifier = Modifier.fillMaxWidth().height(8.dp).clip(RoundedCornerShape(4.dp)),
                            color = MaterialTheme.colorScheme.primary,
                            trackColor = MaterialTheme.colorScheme.surfaceVariant
                        )
                        Spacer(modifier = Modifier.height(4.dp))
                        Text("${(transferProgress * 100).toInt()}%", color = MaterialTheme.colorScheme.onSurfaceVariant, fontSize = 12.sp, modifier = Modifier.fillMaxWidth(), textAlign = TextAlign.End)
                    }
                }
            }

            // Tips section
            item {
                Spacer(modifier = Modifier.height(24.dp))
                Card(
                    modifier = Modifier.fillMaxWidth(),
                    shape = RoundedCornerShape(16.dp),
                    colors = CardDefaults.cardColors(containerColor = MaterialTheme.colorScheme.surfaceVariant.copy(alpha = 0.2f)),
                    border = borderStroke()
                ) {
                    Row(modifier = Modifier.padding(16.dp)) {
                        Box(
                            modifier = Modifier.size(32.dp).clip(CircleShape).background(MaterialTheme.colorScheme.primary.copy(alpha = 0.1f)),
                            contentAlignment = Alignment.Center
                        ) {
                            Icon(Icons.Outlined.Shield, contentDescription = null, tint = MaterialTheme.colorScheme.primary, modifier = Modifier.size(16.dp))
                        }
                        Spacer(modifier = Modifier.width(12.dp))
                        Column {
                            Text("Tips for faster transfer", color = MaterialTheme.colorScheme.onBackground, fontWeight = FontWeight.Bold, fontSize = 14.sp)
                            Spacer(modifier = Modifier.height(4.dp))
                            Text("Make sure both devices have Wi-Fi and are close to each other. Large files may take some time to transfer.", color = MaterialTheme.colorScheme.onSurfaceVariant, fontSize = 12.sp, lineHeight = 18.sp)
                        }
                    }
                }
            }
        }
    }

    if (showSendDialog) {
        AlertDialog(
            onDismissRequest = { showSendDialog = false },
            title = { Text("Select Media to Send") },
            text = {
                LazyColumn(modifier = Modifier.fillMaxWidth().heightIn(max = 300.dp)) {
                    if (completedDownloads.isEmpty()) {
                        item { Text("No downloaded movies found.", color = MaterialTheme.colorScheme.onSurfaceVariant) }
                    }
                    items(completedDownloads) { item ->
                        Row(
                            modifier = Modifier
                                .fillMaxWidth()
                                .clickable {
                                    val file = File(context.filesDir, "downloads/${item.id}.mp4")
                                    if (file.exists() && connectedEndpoint != null) {
                                        p2pManager.sendMovie(connectedEndpoint!!.id, item.id, item.title, item.isMovie, file)
                                    }
                                    showSendDialog = false
                                }
                                .padding(vertical = 12.dp)
                        ) {
                            Text(item.title, color = MaterialTheme.colorScheme.onBackground)
                        }
                    }
                }
            },
            confirmButton = {
                TextButton(onClick = { showSendDialog = false }) { Text("Cancel") }
            }
        )
    }
}

@Composable
private fun borderStroke() = androidx.compose.foundation.BorderStroke(1.dp, MaterialTheme.colorScheme.surfaceVariant.copy(alpha = 0.5f))

@Composable
private fun ContentTypeItem(title: String, icon: ImageVector, isSelected: Boolean, modifier: Modifier = Modifier) {
    Column(
        modifier = modifier
            .aspectRatio(1f)
            .clip(RoundedCornerShape(12.dp))
            .background(if (isSelected) MaterialTheme.colorScheme.primary.copy(alpha = 0.1f) else MaterialTheme.colorScheme.surfaceVariant.copy(alpha = 0.3f))
            .border(
                width = 1.dp,
                color = if (isSelected) MaterialTheme.colorScheme.primary else MaterialTheme.colorScheme.surfaceVariant.copy(alpha = 0.5f),
                shape = RoundedCornerShape(12.dp)
            )
            .clickable { },
        horizontalAlignment = Alignment.CenterHorizontally,
        verticalArrangement = Arrangement.Center
    ) {
        Icon(icon, contentDescription = null, tint = if (isSelected) MaterialTheme.colorScheme.primary else MaterialTheme.colorScheme.onSurfaceVariant)
        Spacer(modifier = Modifier.height(8.dp))
        Text(title, color = if (isSelected) MaterialTheme.colorScheme.primary else MaterialTheme.colorScheme.onSurfaceVariant, fontSize = 12.sp)
    }
}

@Composable
private fun RecentTransferItem(
    title: String,
    typeAndSize: String,
    status: String,
    target: String,
    time: String,
    isSent: Boolean,
    completed: Boolean
) {
    Row(
        modifier = Modifier.fillMaxWidth().padding(vertical = 12.dp),
        verticalAlignment = Alignment.CenterVertically
    ) {
        // Thumbnail placeholder
        Box(
            modifier = Modifier.size(64.dp).clip(RoundedCornerShape(8.dp)).background(MaterialTheme.colorScheme.surfaceVariant),
            contentAlignment = Alignment.Center
        ) {
            Icon(Icons.Default.Movie, contentDescription = null, tint = MaterialTheme.colorScheme.onSurfaceVariant)
        }
        Spacer(modifier = Modifier.width(16.dp))
        Column(modifier = Modifier.weight(1f)) {
            Row(modifier = Modifier.fillMaxWidth(), horizontalArrangement = Arrangement.SpaceBetween) {
                Text(title, color = MaterialTheme.colorScheme.onBackground, fontWeight = FontWeight.Bold, fontSize = 16.sp)
                Text(time, color = MaterialTheme.colorScheme.onSurfaceVariant, fontSize = 12.sp)
            }
            Spacer(modifier = Modifier.height(4.dp))
            Row(verticalAlignment = Alignment.CenterVertically) {
                Text(typeAndSize, color = MaterialTheme.colorScheme.onSurfaceVariant, fontSize = 12.sp)
                Spacer(modifier = Modifier.width(8.dp))
                Icon(if (isSent) Icons.Default.ArrowUpward else Icons.Default.ArrowDownward, contentDescription = null, tint = if (isSent) Color.Red else Color.Blue, modifier = Modifier.size(12.dp))
                Spacer(modifier = Modifier.width(4.dp))
                Text(status, color = if (isSent) Color.Red else Color.Blue, fontSize = 12.sp)
            }
            Spacer(modifier = Modifier.height(4.dp))
            Row(modifier = Modifier.fillMaxWidth(), horizontalArrangement = Arrangement.SpaceBetween, verticalAlignment = Alignment.CenterVertically) {
                Text(target, color = MaterialTheme.colorScheme.onSurfaceVariant, fontSize = 12.sp)
                if (completed) {
                    Row(verticalAlignment = Alignment.CenterVertically) {
                        Icon(Icons.Default.CheckCircle, contentDescription = null, tint = Color.Green, modifier = Modifier.size(12.dp))
                        Spacer(modifier = Modifier.width(4.dp))
                        Text("Completed", color = Color.Green, fontSize = 12.sp)
                    }
                }
            }
        }
    }
}
