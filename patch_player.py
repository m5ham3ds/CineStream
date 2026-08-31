import re

with open("app/src/main/java/com/example/ui/screens/player/PlayerScreen.kt", "r") as f:
    content = f.read()

# 1. Update Top Bar
top_bar_target = """                    // Top Bar
                    Row(
                        modifier = Modifier
                            .fillMaxWidth()
                            .padding(top = 24.dp, start = 24.dp, end = 24.dp)
                            .align(Alignment.TopCenter),
                        verticalAlignment = Alignment.CenterVertically
                    ) {
                        IconButton(onClick = onBack) {
                            Icon(Icons.AutoMirrored.Filled.ArrowBack, contentDescription = "Back", tint = Color.White, modifier = Modifier.size(28.dp))
                        }
                        Spacer(modifier = Modifier.weight(1f))
                        Column(horizontalAlignment = Alignment.CenterHorizontally) {
                            Text("Now Playing", color = Color.White, fontSize = 20.sp, fontWeight = FontWeight.Bold)
                            Spacer(modifier = Modifier.height(4.dp))
                            Text("Episode 1", color = Color.LightGray, fontSize = 14.sp)
                        }
                        Spacer(modifier = Modifier.weight(1f))
                        IconButton(onClick = { /* Menu */ }) {
                            Icon(Icons.Default.MoreVert, contentDescription = "Menu", tint = Color.White, modifier = Modifier.size(28.dp))
                        }
                    }"""

top_bar_replacement = """                    // Top Bar
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
                    }"""
content = content.replace(top_bar_target, top_bar_replacement)

# 2. Update Sliders
sliders_target = """                    // Left Vertical Slider (Brightness)
                    Box(modifier = Modifier.align(Alignment.CenterStart).padding(start = 32.dp)) {
                        VerticalSlider(
                            value = brightness, 
                            onValueChange = { brightness = it }, 
                            icon = Icons.Default.BrightnessMedium
                        )
                    }
                    // Right Vertical Slider (Volume)
                    Box(modifier = Modifier.align(Alignment.CenterEnd).padding(end = 32.dp)) {
                        VerticalSlider(
                            value = volume, 
                            onValueChange = { volume = it }, 
                            icon = Icons.AutoMirrored.Filled.VolumeUp
                        )
                    }"""

sliders_replacement = """                    // Left Vertical Slider (Brightness)
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
                    }"""
content = content.replace(sliders_target, sliders_replacement)

# 3. Update VerticalSlider Component definition
vs_def_target = """@Composable
fun VerticalSlider(value: Float, onValueChange: (Float) -> Unit, icon: ImageVector) {
    Column(horizontalAlignment = Alignment.CenterHorizontally) {
        Icon(icon, contentDescription = null, tint = Color.White, modifier = Modifier.size(28.dp))
        Spacer(modifier = Modifier.height(16.dp))
        Box(
            modifier = Modifier
                .width(40.dp)
                .height(240.dp),
            contentAlignment = Alignment.Center
        ) {
            SimpleSlider(
                value = value,
                onValueChange = onValueChange,
                modifier = Modifier
                    .width(240.dp)
                    .graphicsLayer {
                        rotationZ = -90f
                        transformOrigin = TransformOrigin(0.5f, 0.5f)
                    },
                activeColor = Color.White,
                thumbColor = Color.White,
                inactiveColor = Color.DarkGray.copy(alpha = 0.5f),
                thumbRadius = 18f,
                trackHeight = 10f
            )
        }
    }
}"""

vs_def_replacement = """@Composable
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
}"""
content = content.replace(vs_def_target, vs_def_replacement)

# 4. Update Center Controls
center_target = """                        IconButton(
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
                        }"""

center_replacement = """                        IconButton(
                            onClick = { exoPlayer.seekTo((exoPlayer.currentPosition - 10000).coerceAtLeast(0)) },
                            modifier = Modifier
                                .size(56.dp)
                                .border(1.dp, Color.White.copy(alpha = 0.2f), CircleShape)
                        ) {
                            Icon(Icons.Default.Replay10, contentDescription = "Rewind", tint = Color.White, modifier = Modifier.size(28.dp))
                        }
                        IconButton(
                            onClick = {
                                 if (isPlaying) exoPlayer.pause() else exoPlayer.play() 
                            },
                            modifier = Modifier
                                .size(72.dp)
                                .border(2.dp, Color(0xFFE50914), CircleShape)
                        ) {
                            Icon(
                                if (isPlaying) Icons.Default.Pause else Icons.Default.PlayArrow,
                                contentDescription = "Play/Pause",
                                tint = Color.White,
                                modifier = Modifier.size(36.dp)
                            )
                        }
                        IconButton(
                            onClick = { exoPlayer.seekTo((exoPlayer.currentPosition + 10000).coerceAtMost(exoPlayer.duration)) },
                            modifier = Modifier
                                .size(56.dp)
                                .border(1.dp, Color.White.copy(alpha = 0.2f), CircleShape)
                        ) {
                            Icon(Icons.Default.Forward10, contentDescription = "Forward", tint = Color.White, modifier = Modifier.size(28.dp))
                        }"""
content = content.replace(center_target, center_replacement)

# 5. Clean up Progress Bar Row
progress_target = """                            Text(formatTime(totalDuration), color = Color.White, fontSize = 14.sp)
                            Spacer(modifier = Modifier.width(16.dp))
                            Icon(Icons.Default.PictureInPictureAlt, contentDescription = "PiP", tint = Color.White, modifier = Modifier.size(24.dp).clickable { /* PiP Action */ })
                            Spacer(modifier = Modifier.width(16.dp))
                            Icon(Icons.Default.Fullscreen, contentDescription = "Fullscreen", tint = Color.White, modifier = Modifier.size(28.dp).clickable { /* Fullscreen Action */ })
                        }"""

progress_replacement = """                            Text(formatTime(totalDuration), color = Color.White, fontSize = 14.sp)
                        }"""
content = content.replace(progress_target, progress_replacement)


with open("app/src/main/java/com/example/ui/screens/player/PlayerScreen.kt", "w") as f:
    f.write(content)
