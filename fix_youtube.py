import re

filepath = 'app/src/main/java/com/example/ui/components/YouTubePlayer.kt'
with open(filepath, 'r') as f:
    content = f.read()

content = content.replace('androidx.compose.ui.platform.LocalLifecycleOwner', 'androidx.lifecycle.compose.LocalLifecycleOwner')

# We need to capture the player instance to update it when videoId changes
# Replace the AndroidView block
old_android_view = """        AndroidView(
            modifier = Modifier.fillMaxSize(),
            factory = { ctx ->
                val view = YouTubePlayerView(ctx).apply {
                    enableAutomaticInitialization = false
                }
                lifecycleOwner.lifecycle.addObserver(view)
                view.addFullscreenListener(object : FullscreenListener {
                    override fun onEnterFullscreen(fullscreenView: View, exitFullscreen: () -> Unit) {
                        isFullScreen = true
                        fullScreenView = fullscreenView
                        exitFullscreenAction = exitFullscreen
                        ctx.findActivity()?.requestedOrientation = ActivityInfo.SCREEN_ORIENTATION_SENSOR_LANDSCAPE
                    }
                    override fun onExitFullscreen() {
                        isFullScreen = false
                        fullScreenView = null
                        exitFullscreenAction = null
                        ctx.findActivity()?.requestedOrientation = ActivityInfo.SCREEN_ORIENTATION_UNSPECIFIED
                    }
                })
                val listener = object : AbstractYouTubePlayerListener() {
                    override fun onReady(player: YouTubePlayer) {
                        player.loadVideo(videoId, 0f)
                    }
                }
                
                val options = IFramePlayerOptions.Builder()
                    .controls(1)
                    .fullscreen(1)
                    .build()
                
                view.initialize(listener, options)
                view
            },
            onRelease = {
                it.release()
            }
        )"""

new_android_view = """        var ytPlayer by remember { mutableStateOf<YouTubePlayer?>(null) }
        AndroidView(
            modifier = Modifier.fillMaxSize(),
            factory = { ctx ->
                val view = YouTubePlayerView(ctx).apply {
                    enableAutomaticInitialization = false
                }
                lifecycleOwner.lifecycle.addObserver(view)
                view.addFullscreenListener(object : FullscreenListener {
                    override fun onEnterFullscreen(fullscreenView: View, exitFullscreen: () -> Unit) {
                        isFullScreen = true
                        fullScreenView = fullscreenView
                        exitFullscreenAction = exitFullscreen
                        ctx.findActivity()?.requestedOrientation = ActivityInfo.SCREEN_ORIENTATION_SENSOR_LANDSCAPE
                    }
                    override fun onExitFullscreen() {
                        isFullScreen = false
                        fullScreenView = null
                        exitFullscreenAction = null
                        ctx.findActivity()?.requestedOrientation = ActivityInfo.SCREEN_ORIENTATION_UNSPECIFIED
                    }
                })
                val listener = object : AbstractYouTubePlayerListener() {
                    override fun onReady(player: YouTubePlayer) {
                        ytPlayer = player
                        player.loadVideo(videoId, 0f)
                    }
                }
                
                val options = IFramePlayerOptions.Builder()
                    .controls(1)
                    .fullscreen(1)
                    .build()
                
                view.initialize(listener, options)
                view
            },
            update = { view ->
                ytPlayer?.loadVideo(videoId, 0f)
            },
            onRelease = {
                it.release()
            }
        )"""

content = content.replace(old_android_view, new_android_view)

with open(filepath, 'w') as f:
    f.write(content)

