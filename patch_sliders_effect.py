import re

with open("app/src/main/java/com/example/ui/screens/player/PlayerScreen.kt", "r") as f:
    content = f.read()

target = """    LaunchedEffect(isPlaying) {"""

replacement = """    LaunchedEffect(brightness) {
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
    
    LaunchedEffect(isPlaying) {"""

content = content.replace(target, replacement)

with open("app/src/main/java/com/example/ui/screens/player/PlayerScreen.kt", "w") as f:
    f.write(content)
