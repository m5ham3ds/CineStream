package com.example.ui.screens.share

import android.Manifest
import android.os.Build
import androidx.compose.foundation.background
import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.automirrored.filled.ArrowBack
import androidx.compose.material.icons.filled.Bluetooth
import androidx.compose.material.icons.filled.FileDownload
import androidx.compose.material.icons.filled.FileUpload
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
import com.example.data.model.DownloadItem
import com.example.data.repository.DownloadRepository
import com.example.utils.P2PManager
import com.example.utils.P2PState
import com.google.accompanist.permissions.ExperimentalPermissionsApi
import com.google.accompanist.permissions.rememberMultiplePermissionsState
import kotlinx.coroutines.launch
import java.io.File

@OptIn(ExperimentalPermissionsApi::class, ExperimentalMaterial3Api::class)
@Composable
fun ShareScreen(onBack: () -> Unit) {
    val context = LocalContext.current
    val p2pManager = remember { P2PManager(context) }
    val downloadRepository = remember { DownloadRepository(context) }
    val scope = rememberCoroutineScope()
    
    val p2pState by p2pManager.p2pState.collectAsState()
    val discoveredEndpoints by p2pManager.discoveredEndpoints.collectAsState()
    val connectedEndpoint by p2pManager.connectedEndpoint.collectAsState()
    val transferProgress by p2pManager.transferProgress.collectAsState()
    
    val downloads by downloadRepository.getDownloadItems().collectAsState(initial = emptyList())
    val completedDownloads = downloads.filter { it.isCompleted }

    // Setup receive handler
    LaunchedEffect(Unit) {
        p2pManager.onMovieReceived = { id, title, isMovie ->
            scope.launch {
                downloadRepository.addToDownloads(
                    DownloadItem(id = id, title = title, posterUrl = "", progress = 1f, isMovie = isMovie, isCompleted = true, isPaused = false, quality = "1080p")
                )
            }
        }
    }

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
        topBar = {
            TopAppBar(
                title = { Text("Offline Share") },
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
                .padding(16.dp),
            horizontalAlignment = Alignment.CenterHorizontally
        ) {
            if (!permissionsState.allPermissionsGranted) {
                Icon(Icons.Default.Bluetooth, contentDescription = null, modifier = Modifier.size(64.dp), tint = MaterialTheme.colorScheme.primary)
                Spacer(modifier = Modifier.height(16.dp))
                Text("Nearby Share requires Bluetooth and Location permissions to connect to devices offline.", color = MaterialTheme.colorScheme.onBackground, textAlign = androidx.compose.ui.text.style.TextAlign.Center)
                Spacer(modifier = Modifier.height(16.dp))
                Button(onClick = { permissionsState.launchMultiplePermissionRequest() }) {
                    Text("Grant Permissions")
                }
                return@Column
            }

            // State UI
            Text("Status: ${p2pState.name}", color = MaterialTheme.colorScheme.primary, fontWeight = FontWeight.Bold)
            Spacer(modifier = Modifier.height(24.dp))

            if (p2pState == P2PState.IDLE) {
                Row(modifier = Modifier.fillMaxWidth(), horizontalArrangement = Arrangement.SpaceEvenly) {
                    Button(
                        onClick = { p2pManager.startDiscovery() },
                        colors = ButtonDefaults.buttonColors(containerColor = MaterialTheme.colorScheme.primary)
                    ) {
                        Icon(Icons.Default.FileUpload, contentDescription = null)
                        Spacer(modifier = Modifier.width(8.dp))
                        Text("Send Movie")
                    }
                    
                    Button(
                        onClick = { p2pManager.startAdvertising(android.os.Build.MODEL) },
                        colors = ButtonDefaults.buttonColors(containerColor = MaterialTheme.colorScheme.secondary)
                    ) {
                        Icon(Icons.Default.FileDownload, contentDescription = null)
                        Spacer(modifier = Modifier.width(8.dp))
                        Text("Receive Movie")
                    }
                }
            }

            if (p2pState == P2PState.ADVERTISING) {
                CircularProgressIndicator()
                Spacer(modifier = Modifier.height(16.dp))
                Text("Waiting for sender to connect...", color = MaterialTheme.colorScheme.onSurfaceVariant)
                Spacer(modifier = Modifier.height(16.dp))
                Button(onClick = { p2pManager.stopAll() }) { Text("Cancel") }
            }

            if (p2pState == P2PState.DISCOVERING) {
                CircularProgressIndicator()
                Spacer(modifier = Modifier.height(16.dp))
                Text("Looking for nearby devices...", color = MaterialTheme.colorScheme.onSurfaceVariant)
                
                Spacer(modifier = Modifier.height(24.dp))
                LazyColumn(modifier = Modifier.fillMaxWidth()) {
                    items(discoveredEndpoints) { endpoint ->
                        Card(
                            modifier = Modifier
                                .fillMaxWidth()
                                .padding(vertical = 4.dp)
                                .clickable {
                                    p2pManager.requestConnection(endpoint.id, android.os.Build.MODEL)
                                },
                            colors = CardDefaults.cardColors(containerColor = MaterialTheme.colorScheme.surface)
                        ) {
                            Row(modifier = Modifier.padding(16.dp), verticalAlignment = Alignment.CenterVertically) {
                                Icon(Icons.Default.Bluetooth, contentDescription = null, tint = MaterialTheme.colorScheme.primary)
                                Spacer(modifier = Modifier.width(16.dp))
                                Text(endpoint.name, fontWeight = FontWeight.Bold)
                            }
                        }
                    }
                }
                Spacer(modifier = Modifier.height(16.dp))
                Button(onClick = { p2pManager.stopAll() }) { Text("Cancel") }
            }

            if (p2pState == P2PState.CONNECTED) {
                Icon(Icons.Default.Bluetooth, contentDescription = null, tint = Color.Green, modifier = Modifier.size(64.dp))
                Spacer(modifier = Modifier.height(16.dp))
                Text("Connected to ${connectedEndpoint?.name}", color = MaterialTheme.colorScheme.onBackground)
                Spacer(modifier = Modifier.height(24.dp))
                
                Button(onClick = { showSendDialog = true }) {
                    Text("Select Movie to Send")
                }
                Spacer(modifier = Modifier.height(8.dp))
                Button(onClick = { p2pManager.stopAll() }, colors = ButtonDefaults.buttonColors(containerColor = MaterialTheme.colorScheme.error)) {
                    Text("Disconnect")
                }
            }

            if (p2pState == P2PState.TRANSFERRING) {
                LinearProgressIndicator(progress = { transferProgress }, modifier = Modifier.fillMaxWidth().height(8.dp).clip(RoundedCornerShape(4.dp)))
                Spacer(modifier = Modifier.height(8.dp))
                Text("Transferring: ${(transferProgress * 100).toInt()}%", color = MaterialTheme.colorScheme.onBackground)
            }
        }
    }

    if (showSendDialog) {
        AlertDialog(
            onDismissRequest = { showSendDialog = false },
            title = { Text("Select Movie") },
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
