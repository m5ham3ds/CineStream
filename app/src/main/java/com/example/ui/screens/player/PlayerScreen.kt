@file:OptIn(androidx.compose.material3.ExperimentalMaterial3Api::class)
package com.example.ui.screens.player



import androidx.compose.ui.res.stringResource
import com.example.R
import androidx.annotation.OptIn
import androidx.compose.animation.*
import androidx.compose.runtime.DisposableEffect
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.platform.LocalView
import androidx.core.view.WindowCompat
import androidx.core.view.WindowInsetsCompat
import androidx.core.view.WindowInsetsControllerCompat
import android.app.Activity
import android.content.pm.ActivityInfo
import androidx.compose.material3.ExperimentalMaterial3Api

import androidx.compose.foundation.gestures.detectDragGestures
import androidx.compose.foundation.gestures.detectTapGestures
import androidx.compose.ui.input.pointer.pointerInput
import androidx.compose.foundation.Canvas
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items
import androidx.compose.ui.geometry.Offset
import androidx.compose.ui.geometry.CornerRadius
import androidx.compose.ui.geometry.Size
import androidx.compose.foundation.background
import androidx.compose.foundation.border
import androidx.compose.material.icons.filled.MoreVert
import androidx.compose.material.icons.filled.PictureInPictureAlt
import androidx.compose.material.icons.filled.Fullscreen
import androidx.compose.material.icons.filled.VideoLibrary
import androidx.compose.material.icons.filled.Lock
import androidx.compose.material.icons.filled.LockOpen
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

@OptIn(androidx.media3.common.util.UnstableApi::class, androidx.compose.material3.ExperimentalMaterial3Api::class)
@Composable
@Suppress("OPT_IN_USAGE")
fun PlayerScreen(videoUrl: String, title: String, onBack: () -> Unit) {
    val context = LocalContext.current
    var showDownloadSheet by remember { mutableStateOf(false) }
    var showControls by remember { mutableStateOf(true) }
    var isPlaying by remember { mutableStateOf(true) }
    var currentTime by remember { mutableStateOf(0L) }
    var totalDuration by remember { mutableStateOf(0L) }
    var brightness by remember { mutableStateOf(0.5f) }
    var volume by remember { mutableStateOf(0.5f) }
    var isLocked by remember { mutableStateOf(false) }
    var currentSpeed by remember { mutableStateOf(1f) }
    var currentQuality by remember { mutableStateOf("1080p") }
    var showQualitySheet by remember { mutableStateOf(false) }
    var showEpisodesSheet by remember { mutableStateOf(false) }

    // Force landscape mode for better viewing
    DisposableEffect(Unit) {
        val activity = context as? Activity
        activity?.requestedOrientation = ActivityInfo.SCREEN_ORIENTATION_SENSOR_LANDSCAPE
        
        val window = activity?.window
        var insetsController: WindowInsetsControllerCompat? = null
        if (window != null) {
            insetsController = WindowInsetsControllerCompat(window, window.decorView)
            insetsController.systemBarsBehavior = WindowInsetsControllerCompat.BEHAVIOR_SHOW_TRANSIENT_BARS_BY_SWIPE
            insetsController.hide(androidx.core.view.WindowInsetsCompat.Type.systemBars())
        }
        
        onDispose {
            activity?.requestedOrientation = ActivityInfo.SCREEN_ORIENTATION_UNSPECIFIED
            insetsController?.show(androidx.core.view.WindowInsetsCompat.Type.systemBars())
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

    LaunchedEffect(brightness) {
        val window = (context as? Activity)?.window
        window?.let {
            val lp = it.attributes
            lp.screenBrightness = brightness
            it.attributes = lp
        }
    }
    
    LaunchedEffect(volume) {
        exoPlayer.volume = volume
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
                            .padding(top = 24.dp, start = 24.dp, end = 24.dp)
                            .align(Alignment.TopCenter),
                        verticalAlignment = Alignment.CenterVertically,
                        horizontalArrangement = Arrangement.SpaceBetween
                    ) {
                        Row(verticalAlignment = Alignment.CenterVertically, modifier = Modifier.weight(1f)) {
                            IconButton(onClick = onBack) {
                                Icon(Icons.AutoMirrored.Filled.ArrowBack, contentDescription = "Back", tint = Color.White, modifier = Modifier.size(28.dp))
                            }
                            Spacer(modifier = Modifier.weight(1f))
                            Text("SERVER", color = Color.Gray, fontSize = 14.sp, fontWeight = FontWeight.SemiBold)
                            Spacer(modifier = Modifier.width(4.dp))
                            Icon(Icons.Default.KeyboardArrowDown, contentDescription = null, tint = Color(0xFFE50914), modifier = Modifier.size(16.dp))
                            Spacer(modifier = Modifier.weight(1f))
                        }
                        Column(horizontalAlignment = Alignment.CenterHorizontally) {
                            Text("Now Playing", color = Color.White, fontSize = 20.sp, fontWeight = FontWeight.Bold)
                            Spacer(modifier = Modifier.height(4.dp))
                            Text("Episode 1", color = Color.LightGray, fontSize = 14.sp)
                        }
                        Row(verticalAlignment = Alignment.CenterVertically, modifier = Modifier.weight(1f)) {
                            Spacer(modifier = Modifier.weight(1f))
                            Icon(Icons.Default.KeyboardArrowDown, contentDescription = null, tint = Color(0xFFE50914), modifier = Modifier.size(16.dp))
                            Spacer(modifier = Modifier.width(4.dp))
                            Text("WEBSITE", color = Color.Gray, fontSize = 14.sp, fontWeight = FontWeight.SemiBold)
                            Spacer(modifier = Modifier.weight(1f))
                            IconButton(onClick = { /* Menu */ }) {
                                Icon(Icons.Default.MoreVert, contentDescription = "Menu", tint = Color.White, modifier = Modifier.size(28.dp))
                            }
                        }
                    }

                    // Left Vertical Slider (Brightness)
                    Box(modifier = Modifier.align(Alignment.CenterStart).padding(start = 32.dp)) {
                        VerticalSlider(
                            value = brightness,
                            onValueChange = { brightness = it },
                            topIcon = Icons.Default.BrightnessMedium,
                            bottomIcon = Icons.Default.PictureInPictureAlt
                        )
                    }

                    // Right Vertical Slider (Volume)
                    Box(modifier = Modifier.align(Alignment.CenterEnd).padding(end = 32.dp)) {
                        VerticalSlider(
                            value = volume,
                            onValueChange = { volume = it },
                            topIcon = Icons.AutoMirrored.Filled.VolumeUp,
                            bottomIcon = Icons.Default.Fullscreen
                        )
                    }

                    // Center Playback Controls
                    Row(
                        modifier = Modifier.align(Alignment.Center),
                        verticalAlignment = Alignment.CenterVertically,
                        horizontalArrangement = Arrangement.spacedBy(40.dp)
                    ) {
                        IconButton(
                            onClick = { exoPlayer.seekTo((exoPlayer.currentPosition - 10000).coerceAtLeast(0)) },
                            modifier = Modifier
                                .size(56.dp)
                                .border(1.dp, Color.White.copy(alpha = 0.2f), CircleShape)
                        ) {
                            Icon(Icons.Default.Replay10, contentDescription = "Rewind", tint = Color.White, modifier = Modifier.size(32.dp))
                        }

                        IconButton(
                            onClick = { 
                                if (isPlaying) exoPlayer.pause() else exoPlayer.play() 
                            },
                            modifier = Modifier
                                .size(96.dp)
                                .border(2.dp, Color(0xFFE50914), CircleShape)
                        ) {
                            Icon(
                                if (isPlaying) Icons.Default.Pause else Icons.Default.PlayArrow,
                                contentDescription = "Play/Pause",
                                tint = Color.White,
                                modifier = Modifier.size(48.dp)
                            )
                        }

                        IconButton(
                            onClick = { exoPlayer.seekTo((exoPlayer.currentPosition + 10000).coerceAtMost(exoPlayer.duration)) },
                            modifier = Modifier
                                .size(56.dp)
                                .border(1.dp, Color.White.copy(alpha = 0.2f), CircleShape)
                        ) {
                            Icon(Icons.Default.Forward10, contentDescription = "Forward", tint = Color.White, modifier = Modifier.size(32.dp))
                        }
                    }

                    // Bottom Controls
                    Column(
                        modifier = Modifier
                            .align(Alignment.BottomCenter)
                            .fillMaxWidth()
                            .padding(horizontal = 48.dp, vertical = 24.dp)
                    ) {
                        // Progress Bar Row
                        Row(
                            verticalAlignment = Alignment.CenterVertically,
                            modifier = Modifier.fillMaxWidth()
                        ) {
                            Text(formatTime(currentTime), color = Color.White, fontSize = 14.sp)
                            Spacer(modifier = Modifier.width(16.dp))
                            SimpleSlider(
                                value = if (totalDuration > 0) (currentTime.toFloat() / totalDuration.toFloat()) else 0f,
                                onValueChange = { percent ->
                                    val newPosition = (percent * totalDuration).toLong()
                                    exoPlayer.seekTo(newPosition)
                                    currentTime = newPosition
                                },
                                modifier = Modifier.weight(1f)
                            )
                            Spacer(modifier = Modifier.width(16.dp))
                            Text(formatTime(totalDuration), color = Color.White, fontSize = 14.sp)
                        }

                        Spacer(modifier = Modifier.height(16.dp))

                        // Action Toolbar Row
                        Row(
                            modifier = Modifier.fillMaxWidth(),
                            horizontalArrangement = Arrangement.SpaceEvenly,
                            verticalAlignment = Alignment.CenterVertically
                        ) {
                            BottomAction(icon = Icons.Default.Speed, text = "Speed (${if (currentSpeed == 1f) "1" else currentSpeed}x)") { 
                                val nextSpeed = when(currentSpeed) {
                                    0.5f -> 1f
                                    1f -> 1.5f
                                    1.5f -> 2f
                                    else -> 0.5f
                                }
                                currentSpeed = nextSpeed
                                exoPlayer.setPlaybackSpeed(nextSpeed)
                            }
                            ActionDivider()
                            BottomAction(icon = Icons.Default.Lock, text = "Lock") { isLocked = true }
                            ActionDivider()
                            BottomAction(icon = Icons.Default.VideoLibrary, text = "Episodes") { showEpisodesSheet = true }
                            ActionDivider()
                            QualityAction(currentQuality, onClick = { showQualitySheet = true })
                            ActionDivider()
                            BottomAction(icon = Icons.Default.Download, text = "Download") { showDownloadSheet = true }
                        }
                    }
                }
            }
        }
    }


    if (showQualitySheet) {
        ModalBottomSheet(
            onDismissRequest = { showQualitySheet = false },
            containerColor = Color(0xFF1C1C1E)
        ) {
            Column(modifier = Modifier.padding(16.dp)) {
                Text("Select Quality", color = Color.White, fontSize = 20.sp, fontWeight = FontWeight.Bold)
                Spacer(modifier = Modifier.height(16.dp))
                val qualities = listOf("4K", "1080p", "720p", "480p", "360p")
                qualities.forEach { q ->
                    TextButton(
                        onClick = { 
                            currentQuality = q
                            showQualitySheet = false
                        },
                        modifier = Modifier.fillMaxWidth()
                    ) {
                        Text(q, color = if (q == currentQuality) Color(0xFFE50914) else Color.White)
                    }
                }
                Spacer(modifier = Modifier.height(32.dp))
            }
        }
    }
    
    if (showEpisodesSheet) {
        ModalBottomSheet(
            onDismissRequest = { showEpisodesSheet = false },
            containerColor = Color(0xFF1C1C1E)
        ) {
            Column(modifier = Modifier.padding(16.dp)) {
                Text("Episodes", color = Color.White, fontSize = 20.sp, fontWeight = FontWeight.Bold)
                Spacer(modifier = Modifier.height(16.dp))
                Column {
                    repeat(5) { i ->
                        val epNum = i + 1
                        TextButton(
                            onClick = { showEpisodesSheet = false },
                            modifier = Modifier.fillMaxWidth()
                        ) {
                            Text("Episode $epNum", color = Color.White)
                        }
                    }
                }
                Spacer(modifier = Modifier.height(32.dp))
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
fun VerticalSlider(value: Float, onValueChange: (Float) -> Unit, topIcon: ImageVector, bottomIcon: ImageVector) {
    Column(horizontalAlignment = Alignment.CenterHorizontally) {
        Icon(topIcon, contentDescription = null, tint = Color.White, modifier = Modifier.size(28.dp))
        Spacer(modifier = Modifier.height(16.dp))
        Box(
            modifier = Modifier
                .width(40.dp)
                .height(200.dp),
            contentAlignment = Alignment.Center
        ) {
            SimpleSlider(
                value = value,
                onValueChange = onValueChange,
                modifier = Modifier
                    .width(200.dp)
                    .graphicsLayer {
                        rotationZ = -90f
                        transformOrigin = TransformOrigin(0.5f, 0.5f)
                    },
                activeColor = Color.White,
                thumbColor = Color.White,
                inactiveColor = Color.DarkGray.copy(alpha = 0.5f),
                thumbRadius = 16f,
                trackHeight = 8f
            )
        }
        Spacer(modifier = Modifier.height(16.dp))
        Icon(bottomIcon, contentDescription = null, tint = Color.White, modifier = Modifier.size(28.dp))
    }
}

@Composable
fun BottomAction(icon: ImageVector, text: String, onClick: () -> Unit) {
    Row(
        verticalAlignment = Alignment.CenterVertically,
        modifier = Modifier.clickable(onClick = onClick).padding(8.dp)
    ) {
        Icon(icon, contentDescription = null, tint = Color.White, modifier = Modifier.size(20.dp))
        Spacer(modifier = Modifier.width(8.dp))
        Text(text, color = Color.LightGray, fontSize = 14.sp, fontWeight = FontWeight.Normal)
    }
}

@Composable
fun QualityAction(currentQuality: String, onClick: () -> Unit) {
    Row(
        verticalAlignment = Alignment.CenterVertically,
        modifier = Modifier.clickable(onClick = onClick).padding(8.dp)
    ) {
        Icon(Icons.Default.Settings, contentDescription = null, tint = Color.White, modifier = Modifier.size(20.dp))
        Spacer(modifier = Modifier.width(8.dp))
        Text("Quality", color = Color.LightGray, fontSize = 14.sp, fontWeight = FontWeight.Normal)
        Spacer(modifier = Modifier.width(6.dp))
        Box(
            modifier = Modifier
                .border(1.dp, Color(0xFFE50914), CircleShape)
                .padding(horizontal = 6.dp, vertical = 2.dp)
        ) {
            Text("1080p", color = Color(0xFFE50914), fontSize = 10.sp, fontWeight = FontWeight.Bold)
        }
    }
}

@Composable
fun ActionDivider() {
    Box(
        modifier = Modifier
            .width(1.dp)
            .height(16.dp)
            .background(Color.DarkGray)
    )
}

fun formatTime(timeMs: Long): String {
    if (timeMs < 0) return "00:00"
    val totalSeconds = timeMs / 1000
    val minutes = totalSeconds / 60
    val seconds = totalSeconds % 60
    return String.format("%02d:%02d", minutes, seconds)
}

@Composable
fun SimpleSlider(
    value: Float,
    onValueChange: (Float) -> Unit,
    modifier: Modifier = Modifier,
    activeColor: Color = Color(0xFFE50914),
    inactiveColor: Color = Color.DarkGray,
    thumbColor: Color = Color(0xFFE50914),
    thumbRadius: Float = 12f,
    trackHeight: Float = 8f
) {
    Canvas(
        modifier = modifier
            .fillMaxWidth()
            .height(32.dp) // Touch target height
            .pointerInput(Unit) {
                detectTapGestures { offset ->
                    onValueChange((offset.x / size.width).coerceIn(0f, 1f))
                }
            }
            .pointerInput(Unit) {
                detectDragGestures { change, _ ->
                    onValueChange((change.position.x / size.width).coerceIn(0f, 1f))
                }
            }
    ) {
        val width = size.width
        val height = size.height
        val centerY = height / 2f
        
        // Inactive Track
        drawRoundRect(
            color = inactiveColor,
            topLeft = Offset(0f, centerY - trackHeight / 2f),
            size = Size(width, trackHeight),
            cornerRadius = CornerRadius(trackHeight / 2f)
        )
        
        // Active Track
        drawRoundRect(
            color = activeColor,
            topLeft = Offset(0f, centerY - trackHeight / 2f),
            size = Size(width * value, trackHeight),
            cornerRadius = CornerRadius(trackHeight / 2f)
        )
        
        // Thumb
        drawCircle(
            color = thumbColor,
            radius = thumbRadius,
            center = Offset(width * value, centerY)
        )
    }
}
