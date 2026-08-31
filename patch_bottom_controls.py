import re

with open("app/src/main/java/com/example/ui/screens/player/PlayerScreen.kt", "r") as f:
    content = f.read()

# Update Progress Bar Row
progress_bar_target = """                        // Progress Bar Row
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
                        }"""

progress_bar_replacement = """                        // Progress Bar Row
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
                            Spacer(modifier = Modifier.width(16.dp))
                            Icon(Icons.Default.PictureInPictureAlt, contentDescription = "PiP", tint = Color.White, modifier = Modifier.size(24.dp).clickable { /* PiP Action */ })
                            Spacer(modifier = Modifier.width(16.dp))
                            Icon(Icons.Default.Fullscreen, contentDescription = "Fullscreen", tint = Color.White, modifier = Modifier.size(28.dp).clickable { /* Fullscreen Action */ })
                        }"""
content = content.replace(progress_bar_target, progress_bar_replacement)

with open("app/src/main/java/com/example/ui/screens/player/PlayerScreen.kt", "w") as f:
    f.write(content)
