package com.example.ui.screens.player

import android.app.Activity
import android.content.pm.ActivityInfo
import androidx.annotation.OptIn
import androidx.compose.animation.*
import androidx.compose.foundation.background
import androidx.compose.foundation.clickable
import androidx.compose.foundation.interaction.MutableInteractionSource
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.shape.CircleShape
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.automirrored.filled.VolumeUp
import androidx.compose.material.icons.automirrored.filled.ArrowBack
import androidx.compose.material.icons.filled.*
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.graphics.TransformOrigin
import androidx.compose.ui.graphics.graphicsLayer
import androidx.compose.ui.graphics.vector.ImageVector
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import androidx.compose.ui.viewinterop.AndroidView
import androidx.media3.common.MediaItem
import androidx.media3.common.Player
import androidx.media3.common.util.UnstableApi
import androidx.media3.exoplayer.ExoPlayer
import androidx.media3.ui.PlayerView
import kotlinx.coroutines.delay
import com.example.ui.components.DownloadQualitySheet

@OptIn(UnstableApi::class)
@Composable
fun PlayerScreen(videoUrl: String, onBack: () -> Unit) {
    val context = LocalContext.current
    var showDownloadSheet by remember { mutableStateOf(false) }
    var showControls by remember { mutableStateOf(true) }
    var isPlaying by remember { mutableStateOf(true) }
    var currentTime by remember { mutableStateOf(0L) }
    var totalDuration by remember { mutableStateOf(0L) }
    var brightness by remember { mutableStateOf(0.5f) }
    var volume by remember { mutableStateOf(0.5f) }
    var isLocked by remember { mutableStateOf(false) }

    // Force landscape mode for better viewing
    DisposableEffect(Unit) {
        val activity = context as? Activity
        activity?.requestedOrientation = ActivityInfo.SCREEN_ORIENTATION_SENSOR_LANDSCAPE
        onDispose {
            activity?.requestedOrientation = ActivityInfo.SCREEN_ORIENTATION_UNSPECIFIED
        }
    }

    val exoPlayer = remember {
        ExoPlayer.Builder(context).build().apply {
            val mediaItem = MediaItem.fromUri(videoUrl)
            setMediaItem(mediaItem)
            prepare()
            playWhenReady = true
            addListener(object : Player.Listener {
                override fun onIsPlayingChanged(isPlayingChanged: Boolean) {
                    isPlaying = isPlayingChanged
                }
                override fun onPlaybackStateChanged(state: Int) {
                    if (state == Player.STATE_READY) {
                        totalDuration = duration.coerceAtLeast(0L)
                    }
                }
            })
        }
    }

    LaunchedEffect(isPlaying) {
        while (isPlaying) {
            currentTime = exoPlayer.currentPosition
            delay(1000)
        }
    }

    LaunchedEffect(showControls, isPlaying) {
        if (showControls && isPlaying) {
            delay(4000)
            if (!isLocked) showControls = false
        }
    }

    DisposableEffect(Unit) {
        onDispose {
            exoPlayer.release()
        }
    }

    Box(
        modifier = Modifier
            .fillMaxSize()
            .background(MaterialTheme.colorScheme.background)
            .clickable(
                interactionSource = remember { MutableInteractionSource() },
                indication = null
            ) {
                showControls = !showControls
            }
    ) {
        AndroidView(
            factory = { ctx ->
                PlayerView(ctx).apply {
                    player = exoPlayer
                    useController = false
                }
            },
            modifier = Modifier.fillMaxSize()
        )

        AnimatedVisibility(
            visible = showControls,
            enter = fadeIn(),
            exit = fadeOut(),
            modifier = Modifier.fillMaxSize()
        ) {
            Box(
                modifier = Modifier
                    .fillMaxSize()
                    .background(Color.Black.copy(alpha = 0.5f))
            ) {
                if (isLocked) {
                    // Only show unlock button if locked
                    IconButton(
                        onClick = { isLocked = false; showControls = true },
                        modifier = Modifier
                            .align(Alignment.CenterStart)
                            .padding(32.dp)
                    ) {
                        Icon(Icons.Default.Lock, contentDescription = "Unlock", tint = MaterialTheme.colorScheme.onBackground, modifier = Modifier.size(32.dp))
                    }
                } else {
                    // Full Controls
                    // Top Bar
                    Row(
                        modifier = Modifier
                            .fillMaxWidth()
                            .padding(top = 16.dp, start = 16.dp, end = 16.dp)
                            .align(Alignment.TopCenter),
                        verticalAlignment = Alignment.CenterVertically
                    ) {
                        IconButton(onClick = onBack) {
                            Icon(Icons.AutoMirrored.Filled.ArrowBack, contentDescription = "Back", tint = MaterialTheme.colorScheme.onBackground)
                        }
                        Spacer(modifier = Modifier.weight(1f))
                        Column(horizontalAlignment = Alignment.CenterHorizontally) {
                            Text("Now Playing", color = MaterialTheme.colorScheme.onBackground, fontSize = 18.sp, fontWeight = FontWeight.Bold)
                            Text("Episode 1", color = MaterialTheme.colorScheme.onSurfaceVariant, fontSize = 14.sp)
                        }
                        Spacer(modifier = Modifier.weight(1f))
                        Spacer(modifier = Modifier.width(48.dp)) // Balance the back button
                    }

                    // Left Vertical Slider (Brightness)
                    Box(modifier = Modifier.align(Alignment.CenterStart).padding(start = 24.dp)) {
                        VerticalSlider(value = brightness, onValueChange = { brightness = it }, icon = Icons.Default.BrightnessMedium)
                    }

                    // Right Vertical Slider (Volume)
                    Box(modifier = Modifier.align(Alignment.CenterEnd).padding(end = 24.dp)) {
                        VerticalSlider(value = volume, onValueChange = { volume = it }, icon = Icons.AutoMirrored.Filled.VolumeUp)
                    }

                    // Center Playback Controls
                    Row(
                        modifier = Modifier.align(Alignment.Center),
                        verticalAlignment = Alignment.CenterVertically,
                        horizontalArrangement = Arrangement.spacedBy(48.dp)
                    ) {
                        IconButton(
                            onClick = { exoPlayer.seekTo((exoPlayer.currentPosition - 5000).coerceAtLeast(0)) },
                            modifier = Modifier.size(56.dp)
                        ) {
                            Box(contentAlignment = Alignment.Center) {
                                Icon(Icons.Default.Refresh, contentDescription = "Rewind", tint = MaterialTheme.colorScheme.onBackground, modifier = Modifier.size(48.dp).graphicsLayer { scaleX = -1f })
                                Text("5", color = MaterialTheme.colorScheme.onBackground, fontSize = 12.sp, fontWeight = FontWeight.Bold)
                            }
                        }

                        IconButton(
                            onClick = { 
                                if (isPlaying) exoPlayer.pause() else exoPlayer.play() 
                            },
                            modifier = Modifier.size(80.dp)
                        ) {
                            Icon(
                                if (isPlaying) Icons.Default.Pause else Icons.Default.PlayArrow,
                                contentDescription = "Play/Pause",
                                tint = MaterialTheme.colorScheme.onBackground,
                                modifier = Modifier.size(64.dp)
                            )
                        }

                        IconButton(
                            onClick = { exoPlayer.seekTo((exoPlayer.currentPosition + 5000).coerceAtMost(exoPlayer.duration)) },
                            modifier = Modifier.size(56.dp)
                        ) {
                            Box(contentAlignment = Alignment.Center) {
                                Icon(Icons.Default.Refresh, contentDescription = "Forward", tint = MaterialTheme.colorScheme.onBackground, modifier = Modifier.size(48.dp))
                                Text("5", color = MaterialTheme.colorScheme.onBackground, fontSize = 12.sp, fontWeight = FontWeight.Bold)
                            }
                        }
                    }

                    // Bottom Controls
                    Column(
                        modifier = Modifier
                            .align(Alignment.BottomCenter)
                            .fillMaxWidth()
                            .padding(horizontal = 24.dp, vertical = 16.dp)
                    ) {
                        // Progress Bar Row
                        Row(
                            verticalAlignment = Alignment.CenterVertically,
                            modifier = Modifier.fillMaxWidth()
                        ) {
                            Text(formatTime(currentTime), color = MaterialTheme.colorScheme.onBackground, fontSize = 14.sp)
                            Spacer(modifier = Modifier.width(12.dp))
                            Slider(
                                value = if (totalDuration > 0) (currentTime.toFloat() / totalDuration.toFloat()) else 0f,
                                onValueChange = { percent ->
                                    val newPosition = (percent * totalDuration).toLong()
                                    exoPlayer.seekTo(newPosition)
                                    currentTime = newPosition
                                },
                                modifier = Modifier.weight(1f),
                                colors = SliderDefaults.colors(
                                    thumbColor = Color(0xFF00A8FF),
                                    activeTrackColor = Color(0xFF00A8FF),
                                    inactiveTrackColor = MaterialTheme.colorScheme.onSurfaceVariant.copy(alpha = 0.5f)
                                )
                            )
                            Spacer(modifier = Modifier.width(12.dp))
                            Text(formatTime(totalDuration), color = MaterialTheme.colorScheme.onBackground, fontSize = 14.sp)
                        }

                        Spacer(modifier = Modifier.height(8.dp))

                        // Action Toolbar Row
                        Row(
                            modifier = Modifier.fillMaxWidth(),
                            horizontalArrangement = Arrangement.SpaceBetween,
                            verticalAlignment = Alignment.CenterVertically
                        ) {
                            BottomAction(icon = Icons.Default.Speed, text = "Speed (1x)") { 
                                val newSpeed = if (exoPlayer.playbackParameters.speed == 1f) 1.5f else 1f
                                exoPlayer.setPlaybackSpeed(newSpeed)
                            }
                            BottomAction(icon = Icons.Default.LockOpen, text = "Lock") { isLocked = true }
                            BottomAction(icon = Icons.Default.Settings, text = "Quality (المتوفرة)") { /* Future implementation */ }
                            BottomAction(icon = Icons.Default.Download, text = "Download") { showDownloadSheet = true }
                            BottomAction(icon = null, text = "+85 s") { 
                                exoPlayer.seekTo((exoPlayer.currentPosition + 85000).coerceAtMost(exoPlayer.duration))
                            }
                        }
                    }
                }
            }
        }
    }

    if (showDownloadSheet) {
        DownloadQualitySheet(
            onDismiss = { showDownloadSheet = false },
            onQualitySelected = { quality ->
                android.widget.Toast.makeText(context, "Downloading in $quality...", android.widget.Toast.LENGTH_SHORT).show()
                showDownloadSheet = false
            }
        )
    }
}

@Composable
fun VerticalSlider(value: Float, onValueChange: (Float) -> Unit, icon: ImageVector) {
    Column(horizontalAlignment = Alignment.CenterHorizontally) {
        Icon(icon, contentDescription = null, tint = MaterialTheme.colorScheme.onBackground)
        Spacer(modifier = Modifier.height(16.dp))
        Box(
            modifier = Modifier
                .width(40.dp)
                .height(120.dp),
            contentAlignment = Alignment.Center
        ) {
            Slider(
                value = value,
                onValueChange = onValueChange,
                modifier = Modifier
                    .width(120.dp)
                    .graphicsLayer {
                        rotationZ = -90f
                        transformOrigin = TransformOrigin(0.5f, 0.5f)
                    },
                colors = SliderDefaults.colors(
                    thumbColor = MaterialTheme.colorScheme.onBackground,
                    activeTrackColor = MaterialTheme.colorScheme.onBackground,
                    inactiveTrackColor = MaterialTheme.colorScheme.onSurfaceVariant.copy(alpha = 0.5f)
                )
            )
        }
    }
}

@Composable
fun BottomAction(icon: ImageVector?, text: String, onClick: () -> Unit) {
    Row(
        verticalAlignment = Alignment.CenterVertically,
        modifier = Modifier.clickable(onClick = onClick).padding(8.dp)
    ) {
        if (icon != null) {
            Icon(icon, contentDescription = null, tint = MaterialTheme.colorScheme.onBackground, modifier = Modifier.size(20.dp))
            Spacer(modifier = Modifier.width(6.dp))
        }
        Text(text, color = MaterialTheme.colorScheme.onBackground, fontSize = 14.sp, fontWeight = FontWeight.Medium)
    }
}

fun formatTime(timeMs: Long): String {
    if (timeMs < 0) return "00:00"
    val totalSeconds = timeMs / 1000
    val minutes = totalSeconds / 60
    val seconds = totalSeconds % 60
    return String.format("%02d:%02d", minutes, seconds)
}
