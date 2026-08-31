import re

with open("app/src/main/java/com/example/ui/screens/player/PlayerScreen.kt", "r") as f:
    content = f.read()

# 1. Update VerticalSlider definition
slider_def_target = """fun VerticalSlider(value: Float, onValueChange: (Float) -> Unit, topIcon: ImageVector, bottomIcon: ImageVector) {
    Column(horizontalAlignment = Alignment.CenterHorizontally) {
        Icon(topIcon, contentDescription = null, tint = Color.White, modifier = Modifier.size(24.dp))
        Spacer(modifier = Modifier.height(16.dp))
        Box(
            modifier = Modifier
                .width(40.dp)
                .height(120.dp),
            contentAlignment = Alignment.Center
        ) {
            SimpleSlider(
                value = value,
                onValueChange = onValueChange,
                modifier = Modifier
                    .width(120.dp)
                    .graphicsLayer {
                        rotationZ = -90f
                        transformOrigin = TransformOrigin(0.5f, 0.5f)
                    },
                activeColor = Color.White,
                thumbColor = Color.White,
                inactiveColor = Color.DarkGray.copy(alpha = 0.5f),
                thumbRadius = 14f,
                trackHeight = 6f
            )
        }
        Spacer(modifier = Modifier.height(16.dp))
        Icon(bottomIcon, contentDescription = null, tint = Color.White, modifier = Modifier.size(24.dp))
    }
}"""

slider_def_replacement = """fun VerticalSlider(value: Float, onValueChange: (Float) -> Unit, icon: ImageVector) {
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

content = content.replace(slider_def_target, slider_def_replacement)

# 2. Update VerticalSlider usages
brightness_target = """                    Box(modifier = Modifier.align(Alignment.CenterStart).padding(start = 32.dp)) {
                        VerticalSlider(
                            value = brightness, 
                            onValueChange = { brightness = it }, 
                            topIcon = Icons.Default.BrightnessMedium,
                            bottomIcon = Icons.Default.PictureInPictureAlt
                        )
                    }"""
brightness_replacement = """                    Box(modifier = Modifier.align(Alignment.CenterStart).padding(start = 32.dp)) {
                        VerticalSlider(
                            value = brightness, 
                            onValueChange = { brightness = it }, 
                            icon = Icons.Default.BrightnessMedium
                        )
                    }"""
content = content.replace(brightness_target, brightness_replacement)

volume_target = """                    Box(modifier = Modifier.align(Alignment.CenterEnd).padding(end = 32.dp)) {
                        VerticalSlider(
                            value = volume, 
                            onValueChange = { volume = it }, 
                            topIcon = Icons.AutoMirrored.Filled.VolumeUp,
                            bottomIcon = Icons.Default.Fullscreen
                        )
                    }"""
volume_replacement = """                    Box(modifier = Modifier.align(Alignment.CenterEnd).padding(end = 32.dp)) {
                        VerticalSlider(
                            value = volume, 
                            onValueChange = { volume = it }, 
                            icon = Icons.AutoMirrored.Filled.VolumeUp
                        )
                    }"""
content = content.replace(volume_target, volume_replacement)

# 3. Update Center Playback Controls sizes
center_controls_target = """                    // Center Playback Controls
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
                    }"""

center_controls_replacement = """                    // Center Playback Controls
                    Row(
                        modifier = Modifier.align(Alignment.Center),
                        verticalAlignment = Alignment.CenterVertically,
                        horizontalArrangement = Arrangement.spacedBy(40.dp)
                    ) {
                        IconButton(
                            onClick = { exoPlayer.seekTo((exoPlayer.currentPosition - 10000).coerceAtLeast(0)) },
                            modifier = Modifier
                                .size(48.dp)
                                .border(1.dp, Color.White.copy(alpha = 0.2f), CircleShape)
                        ) {
                            Icon(Icons.Default.Replay10, contentDescription = "Rewind", tint = Color.White, modifier = Modifier.size(24.dp))
                        }
                        IconButton(
                            onClick = {
                                 if (isPlaying) exoPlayer.pause() else exoPlayer.play() 
                            },
                            modifier = Modifier
                                .size(64.dp)
                                .border(2.dp, Color(0xFFE50914), CircleShape)
                        ) {
                            Icon(
                                if (isPlaying) Icons.Default.Pause else Icons.Default.PlayArrow,
                                contentDescription = "Play/Pause",
                                tint = Color.White,
                                modifier = Modifier.size(32.dp)
                            )
                        }
                        IconButton(
                            onClick = { exoPlayer.seekTo((exoPlayer.currentPosition + 10000).coerceAtMost(exoPlayer.duration)) },
                            modifier = Modifier
                                .size(48.dp)
                                .border(1.dp, Color.White.copy(alpha = 0.2f), CircleShape)
                        ) {
                            Icon(Icons.Default.Forward10, contentDescription = "Forward", tint = Color.White, modifier = Modifier.size(24.dp))
                        }
                    }"""
content = content.replace(center_controls_target, center_controls_replacement)

with open("app/src/main/java/com/example/ui/screens/player/PlayerScreen.kt", "w") as f:
    f.write(content)
