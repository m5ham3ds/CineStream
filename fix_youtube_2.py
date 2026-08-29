import re

filepath = 'app/src/main/java/com/example/ui/components/YouTubePlayer.kt'
with open(filepath, 'r') as f:
    content = f.read()

new_android_view = """        var ytPlayer by remember { mutableStateOf<YouTubePlayer?>(null) }
        var currentVideoId by remember { mutableStateOf("") }
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
                        currentVideoId = videoId
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
                if (ytPlayer != null && currentVideoId != videoId) {
                    currentVideoId = videoId
                    ytPlayer?.loadVideo(videoId, 0f)
                }
            },
            onRelease = {
                it.release()
            }
        )"""

# replace the block again
content = re.sub(r'        var ytPlayer.*?onRelease = \{\n                it\.release\(\)\n            \}\n        \)', new_android_view, content, flags=re.DOTALL)

with open(filepath, 'w') as f:
    f.write(content)

